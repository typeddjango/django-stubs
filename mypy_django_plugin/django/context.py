import os
from collections import defaultdict
from contextlib import contextmanager
from typing import Dict, Iterator, Optional, Set, TYPE_CHECKING, Tuple, Type, Union

from django.core.exceptions import FieldError
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.sql.query import Query
from django.utils.functional import cached_property
from mypy.checker import TypeChecker
from mypy.types import AnyType, Instance, Type as MypyType, TypeOfAny

from django.db.models.fields import AutoField, CharField, Field
from mypy_django_plugin.lib import helpers

try:
    from django.contrib.postgres.fields import ArrayField
except ImportError:
    class ArrayField:  # type: ignore
        pass

if TYPE_CHECKING:
    from django.apps.registry import Apps  # noqa: F401
    from django.conf import LazySettings  # noqa: F401


@contextmanager
def temp_environ():
    """Allow the ability to set os.environ temporarily"""
    environ = dict(os.environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(environ)


def initialize_django(settings_module: str) -> Tuple['Apps', 'LazySettings']:
    with temp_environ():
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

        def noop_class_getitem(cls, key):
            return cls

        from django.db import models

        models.QuerySet.__class_getitem__ = classmethod(noop_class_getitem)  # type: ignore
        models.Manager.__class_getitem__ = classmethod(noop_class_getitem)  # type: ignore

        from django.conf import settings
        from django.apps import apps

        apps.get_models.cache_clear()  # type: ignore
        apps.get_swappable_settings_name.cache_clear()  # type: ignore

        if not settings.configured:
            settings._setup()

        apps.populate(settings.INSTALLED_APPS)

    assert apps.apps_ready
    assert settings.configured

    return apps, settings


class DjangoFieldsContext:
    def __init__(self, django_context: 'DjangoContext') -> None:
        self.django_context = django_context

    def get_attname(self, field: Field) -> str:
        attname = field.attname
        return attname

    def get_field_nullability(self, field: Field, method: Optional[str]) -> bool:
        nullable = field.null
        if not nullable and isinstance(field, CharField) and field.blank:
            return True
        if method == '__init__':
            if field.primary_key or isinstance(field, ForeignKey):
                return True
        if method == 'create':
            if isinstance(field, AutoField):
                return True
        if field.has_default():
            return True
        return nullable

    def get_field_set_type(self, api: TypeChecker, field: Field, *, method: str) -> MypyType:
        """ Get a type of __set__ for this specific Django field. """
        target_field = field
        if isinstance(field, ForeignKey):
            target_field = field.target_field

        field_info = helpers.lookup_class_typeinfo(api, target_field.__class__)
        if field_info is None:
            return AnyType(TypeOfAny.from_error)

        field_set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
                                                             is_nullable=self.get_field_nullability(field, method))
        if isinstance(target_field, ArrayField):
            argument_field_type = self.get_field_set_type(api, target_field.base_field, method=method)
            field_set_type = helpers.convert_any_to_type(field_set_type, argument_field_type)
        return field_set_type

    def get_field_get_type(self, api: TypeChecker, field: Field, *, method: str) -> MypyType:
        """ Get a type of __get__ for this specific Django field. """
        field_info = helpers.lookup_class_typeinfo(api, field.__class__)
        if field_info is None:
            return AnyType(TypeOfAny.unannotated)

        is_nullable = self.get_field_nullability(field, method)
        if isinstance(field, RelatedField):
            related_model_cls = self.django_context.fields_context.get_related_model_cls(field)

            if method == 'values':
                primary_key_field = self.django_context.get_primary_key_field(related_model_cls)
                return self.get_field_get_type(api, primary_key_field, method=method)

            model_info = helpers.lookup_class_typeinfo(api, related_model_cls)
            if model_info is None:
                return AnyType(TypeOfAny.unannotated)

            return Instance(model_info, [])
        else:
            return helpers.get_private_descriptor_type(field_info, '_pyi_private_get_type',
                                                       is_nullable=is_nullable)

    def get_related_model_cls(self, field: Union[RelatedField, ForeignObjectRel]) -> Type[Model]:
        if isinstance(field, RelatedField):
            related_model_cls = field.remote_field.model
        else:
            related_model_cls = field.field.model

        if isinstance(related_model_cls, str):
            if related_model_cls == 'self':
                # same model
                related_model_cls = field.model
            elif '.' not in related_model_cls:
                # same file model
                related_model_fullname = field.model.__module__ + '.' + related_model_cls
                related_model_cls = self.django_context.get_model_class_by_fullname(related_model_fullname)
            else:
                related_model_cls = self.django_context.apps_registry.get_model(related_model_cls)

        return related_model_cls


class DjangoLookupsContext:
    def __init__(self, django_context: 'DjangoContext'):
        self.django_context = django_context

    def resolve_lookup(self, model_cls: Type[Model], lookup: str) -> Field:
        query = Query(model_cls)
        lookup_parts, field_parts, is_expression = query.solve_lookup_type(lookup)
        if lookup_parts:
            raise FieldError('Lookups not supported yet')

        currently_observed_model = model_cls
        current_field = None
        for field_part in field_parts:
            if field_part == 'pk':
                return self.django_context.get_primary_key_field(currently_observed_model)

            current_field = currently_observed_model._meta.get_field(field_part)
            if not isinstance(current_field, (ForeignObjectRel, RelatedField)):
                continue

            currently_observed_model = self.django_context.fields_context.get_related_model_cls(current_field)
            if isinstance(current_field, ForeignObjectRel):
                current_field = self.django_context.get_primary_key_field(currently_observed_model)

        # if it is None, solve_lookup_type() will fail earlier
        assert current_field is not None
        return current_field


class DjangoContext:
    def __init__(self, django_settings_module: str) -> None:
        self.fields_context = DjangoFieldsContext(self)
        self.lookups_context = DjangoLookupsContext(self)

        self.django_settings_module = django_settings_module

        apps, settings = initialize_django(self.django_settings_module)
        self.apps_registry = apps
        self.settings = settings

    @cached_property
    def model_modules(self) -> Dict[str, Set[Type[Model]]]:
        """ All modules that contain Django models. """
        if self.apps_registry is None:
            return {}

        modules: Dict[str, Set[Type[Model]]] = defaultdict(set)
        for concrete_model_cls in self.apps_registry.get_models():
            modules[concrete_model_cls.__module__].add(concrete_model_cls)
            # collect abstract=True models
            for model_cls in concrete_model_cls.mro()[1:]:
                if (issubclass(model_cls, Model)
                        and hasattr(model_cls, '_meta')
                        and model_cls._meta.abstract):
                    modules[model_cls.__module__].add(model_cls)
        return modules

    def get_model_class_by_fullname(self, fullname: str) -> Optional[Type[Model]]:
        # Returns None if Model is abstract
        module, _, model_cls_name = fullname.rpartition('.')
        for model_cls in self.model_modules.get(module, set()):
            if model_cls.__name__ == model_cls_name:
                return model_cls
        return None

    def get_model_fields(self, model_cls: Type[Model]) -> Iterator[Field]:
        for field in model_cls._meta.get_fields():
            if isinstance(field, Field):
                yield field

    def get_model_relations(self, model_cls: Type[Model]) -> Iterator[ForeignObjectRel]:
        for field in model_cls._meta.get_fields():
            if isinstance(field, ForeignObjectRel):
                yield field

    def get_primary_key_field(self, model_cls: Type[Model]) -> Field:
        for field in model_cls._meta.get_fields():
            if isinstance(field, Field):
                if field.primary_key:
                    return field
        raise ValueError('No primary key defined')

    def get_expected_types(self, api: TypeChecker, model_cls: Type[Model], *, method: str) -> Dict[str, MypyType]:
        from django.contrib.contenttypes.fields import GenericForeignKey

        expected_types = {}
        # add pk if not abstract=True
        if not model_cls._meta.abstract:
            primary_key_field = self.get_primary_key_field(model_cls)
            field_set_type = self.fields_context.get_field_set_type(api, primary_key_field, method=method)
            expected_types['pk'] = field_set_type

        for field in model_cls._meta.get_fields():
            if isinstance(field, Field):
                field_name = field.attname
                field_set_type = self.fields_context.get_field_set_type(api, field, method=method)
                expected_types[field_name] = field_set_type

                if isinstance(field, ForeignKey):
                    field_name = field.name
                    foreign_key_info = helpers.lookup_class_typeinfo(api, field.__class__)
                    if foreign_key_info is None:
                        # maybe there's no type annotation for the field
                        expected_types[field_name] = AnyType(TypeOfAny.unannotated)
                        continue

                    related_model = self.fields_context.get_related_model_cls(field)
                    if related_model._meta.proxy_for_model is not None:
                        related_model = related_model._meta.proxy_for_model

                    related_model_info = helpers.lookup_class_typeinfo(api, related_model)
                    if related_model_info is None:
                        expected_types[field_name] = AnyType(TypeOfAny.unannotated)
                        continue

                    is_nullable = self.fields_context.get_field_nullability(field, method)
                    foreign_key_set_type = helpers.get_private_descriptor_type(foreign_key_info,
                                                                               '_pyi_private_set_type',
                                                                               is_nullable=is_nullable)
                    model_set_type = helpers.convert_any_to_type(foreign_key_set_type,
                                                                 Instance(related_model_info, []))

                    expected_types[field_name] = model_set_type

            elif isinstance(field, GenericForeignKey):
                # it's generic, so cannot set specific model
                field_name = field.name
                gfk_info = helpers.lookup_class_typeinfo(api, field.__class__)
                gfk_set_type = helpers.get_private_descriptor_type(gfk_info, '_pyi_private_set_type',
                                                                   is_nullable=True)
                expected_types[field_name] = gfk_set_type

        return expected_types
