import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, TYPE_CHECKING, Tuple, Type

from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.utils.functional import cached_property
from mypy.checker import TypeChecker
from mypy.types import Instance, Type as MypyType
from pytest_mypy.utils import temp_environ

from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField, Field
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy_django_plugin_newsemanal.lib import helpers

if TYPE_CHECKING:
    from django.apps.registry import Apps
    from django.conf import LazySettings


@dataclass
class DjangoPluginConfig:
    ignore_missing_settings: bool = False
    ignore_missing_model_attributes: bool = False


def initialize_django(settings_module: str) -> Tuple['Apps', 'LazySettings']:
    with temp_environ():
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

        def noop_class_getitem(cls, key):
            return cls

        from django.db import models

        models.QuerySet.__class_getitem__ = classmethod(noop_class_getitem)
        models.Manager.__class_getitem__ = classmethod(noop_class_getitem)

        from django.conf import settings
        from django.apps import apps

        apps.get_models.cache_clear()
        apps.get_swappable_settings_name.cache_clear()

        apps.populate(settings.INSTALLED_APPS)

    assert apps.apps_ready
    assert settings.configured

    return apps, settings


class DjangoFieldsContext:
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
        if field.has_default():
            return True
        return nullable

    def get_field_set_type(self, api: TypeChecker, field: Field, method: str) -> MypyType:
        target_field = field
        if isinstance(field, ForeignKey):
            target_field = field.target_field

        field_info = helpers.lookup_class_typeinfo(api, target_field.__class__)
        field_set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
                                                             is_nullable=self.get_field_nullability(field, method))
        if isinstance(target_field, ArrayField):
            argument_field_type = self.get_field_set_type(api, target_field.base_field, method)
            field_set_type = helpers.convert_any_to_type(field_set_type, argument_field_type)
        return field_set_type


class DjangoContext:
    def __init__(self, plugin_toml_config: Optional[Dict[str, Any]]) -> None:
        self.config = DjangoPluginConfig()
        self.fields_context = DjangoFieldsContext()

        self.django_settings_module = None
        if plugin_toml_config:
            self.config.ignore_missing_settings = plugin_toml_config.get('ignore_missing_settings', False)
            self.config.ignore_missing_model_attributes = plugin_toml_config.get('ignore_missing_model_attributes', False)
            self.django_settings_module = plugin_toml_config.get('django_settings_module', None)

        self.apps_registry: Optional[Dict[str, str]] = None
        self.settings: LazySettings = None
        if self.django_settings_module:
            apps, settings = initialize_django(self.django_settings_module)
            self.apps_registry = apps
            self.settings = settings

    @cached_property
    def model_modules(self) -> Dict[str, List[Type[Model]]]:
        """ All modules that contain Django models. """
        if self.apps_registry is None:
            return {}

        modules: Dict[str, List[Type[Model]]] = defaultdict(list)
        for model_cls in self.apps_registry.get_models():
            modules[model_cls.__module__].append(model_cls)
        return modules

    def get_model_class_by_fullname(self, fullname: str) -> Optional[Type[Model]]:
        # Returns None if Model is abstract
        module, _, model_cls_name = fullname.rpartition('.')
        for model_cls in self.model_modules.get(module, []):
            if model_cls.__name__ == model_cls_name:
                return model_cls

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

    def get_expected_types(self, api: TypeChecker, model_cls: Type[Model], method: str) -> Dict[str, MypyType]:
        expected_types = {}
        if method == '__init__':
            # add pk
            primary_key_field = self.get_primary_key_field(model_cls)
            field_set_type = self.fields_context.get_field_set_type(api, primary_key_field, method)
            expected_types['pk'] = field_set_type

        for field in self.get_model_fields(model_cls):
            field_name = field.attname
            field_set_type = self.fields_context.get_field_set_type(api, field, method)
            expected_types[field_name] = field_set_type

            if isinstance(field, ForeignKey):
                field_name = field.name
                foreign_key_info = helpers.lookup_class_typeinfo(api, field.__class__)
                related_model_info = helpers.lookup_class_typeinfo(api, field.related_model)
                is_nullable = self.fields_context.get_field_nullability(field, method)
                foreign_key_set_type = helpers.get_private_descriptor_type(foreign_key_info,
                                                                           '_pyi_private_set_type',
                                                                           is_nullable=is_nullable)
                model_set_type = helpers.convert_any_to_type(foreign_key_set_type,
                                                             Instance(related_model_info, []))
                expected_types[field_name] = model_set_type
        return expected_types
