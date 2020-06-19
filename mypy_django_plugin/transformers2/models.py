from abc import abstractmethod
from typing import Optional, Type

from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateField, DateTimeField
from django.db.models.fields.related import ForeignKey, OneToOneField
from mypy.nodes import (
    ARG_STAR2, MDEF, Argument, SymbolTableNode, TypeInfo, Var,
)
from mypy.plugin import ClassDefContext
from mypy.plugins import common
from mypy.semanal import dummy_context
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import fullnames, helpers, sem_helpers
from mypy_django_plugin.transformers2 import fields, new_helpers


class TransformModelClassCallback(helpers.ClassDefPluginCallback):
    def get_real_manager_fullname(self, manager_fullname: str) -> str:
        model_info = self.lookup_typeinfo_or_defer(fullnames.MODEL_CLASS_FULLNAME)
        assert model_info is not None
        real_manager_fullname = model_info.metadata.get('managers', {}).get(manager_fullname, manager_fullname)
        return real_manager_fullname

    def modify_class_defn(self) -> None:
        model_cls = self.django_context.get_model_class_by_fullname(self.class_defn.fullname)
        if model_cls is None:
            return None
        return self.modify_model_class_defn(model_cls)

    def add_new_model_attribute(self, name: str, typ: MypyType, force_replace: bool = False) -> None:
        model_info = self.class_defn.info
        if name in model_info.names and not force_replace:
            raise ValueError('Attribute already exists on the model')

        var = Var(name, type=typ)
        var.info = model_info
        var._fullname = self.semanal_api.qualified_name(name)
        var.is_initialized_in_class = True

        sym = SymbolTableNode(MDEF, var, plugin_generated=True)
        error_context = None if force_replace else dummy_context()
        added = self.semanal_api.add_symbol_table_node(name, sym, context=error_context)
        assert added

    def lookup_typeinfo_for_class_or_defer(self, klass: type, *,
                                           reason_for_defer: Optional[str] = None) -> Optional[TypeInfo]:
        manager_cls_fullname = helpers.get_class_fullname(klass)
        return self.lookup_typeinfo_or_defer(manager_cls_fullname,
                                             reason_for_defer=reason_for_defer)

    @abstractmethod
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        raise NotImplementedError


class AddDefaultManagerCallback(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        if ('_default_manager' in self.class_defn.info.names
                or runtime_model_cls._meta.default_manager is None):
            return None

        runtime_default_manager_class = runtime_model_cls._meta.default_manager.__class__
        runtime_manager_cls_fullname = new_helpers.get_class_fullname(runtime_default_manager_class)
        manager_cls_fullname = self.get_real_manager_fullname(runtime_manager_cls_fullname)

        default_manager_info = self.lookup_typeinfo_or_defer(manager_cls_fullname)
        if default_manager_info is None:
            if getattr(runtime_model_cls._meta.default_manager, '_built_with_as_manager', False):
                # it's a Model.as_manager() class and will cause TypeNotFound exception without proper support
                # fallback to Any for now to avoid false positives
                self.add_new_model_attribute('_default_manager', AnyType(TypeOfAny.implementation_artifact))
            return

        self.add_new_model_attribute('_default_manager',
                                     Instance(default_manager_info, [Instance(self.class_defn.info, [])]))


class AddManagersCallback(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[models.Model]) -> None:
        for manager_name, manager in runtime_model_cls._meta.managers_map.items():
            if manager_name in self.class_defn.info.names:
                # already defined on the current model class, in file or at a previous iteration
                continue

            manager_info = self.lookup_typeinfo_for_class_or_defer(manager.__class__)
            if manager_info is None:
                continue

            manager_type = Instance(manager_info, [Instance(self.class_defn.info, [])])
            self.add_new_model_attribute(manager_name, manager_type)


class AddPrimaryKeyIfDoesNotExist(TransformModelClassCallback):
    """
    Adds default primary key to models which does not define their own.
        class User(models.Model):
            name = models.TextField()
    """

    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        auto_pk_field = runtime_model_cls._meta.auto_field
        if auto_pk_field is None:
            # defined explicitly
            return None
        auto_pk_field_name = auto_pk_field.attname
        if auto_pk_field_name in self.class_defn.info.names:
            # added on previous iteration
            return None

        auto_pk_field_info = self.lookup_typeinfo_for_class_or_defer(auto_pk_field.__class__)
        if auto_pk_field_info is None:
            return None

        self.add_new_model_attribute(auto_pk_field_name,
                                     fields.get_field_type(auto_pk_field_info, is_nullable=False))


class AddRelatedManagersCallback(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        for reverse_manager_name, relation in self.django_context.get_model_relations(runtime_model_cls):
            if (reverse_manager_name is None
                    or reverse_manager_name in self.class_defn.info.names):
                continue

            self.add_new_model_attribute(reverse_manager_name, AnyType(TypeOfAny.implementation_artifact))


class AddForeignPrimaryKeys(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        for field in runtime_model_cls._meta.get_fields():
            if not isinstance(field, (OneToOneField, ForeignKey)):
                continue
            rel_pk_field_name = field.attname
            if rel_pk_field_name in self.class_defn.info.names:
                continue

            related_model_cls = self.django_context.get_field_related_model_cls(field)
            if related_model_cls is None:
                field_sym = self.class_defn.info.get(field.name)
                if field_sym is not None and field_sym.node is not None:
                    error_context = field_sym.node
                else:
                    error_context = self.class_defn  # type: ignore
                self.semanal_api.fail(f'Cannot find model {field.related_model!r} '
                                      f'referenced in field {field.name!r} ',
                                      ctx=error_context)
                self.add_new_model_attribute(rel_pk_field_name, AnyType(TypeOfAny.from_error))
                continue
            if related_model_cls._meta.abstract:
                continue

            rel_pk_field = self.django_context.get_primary_key_field(related_model_cls)
            rel_pk_field_info = self.lookup_typeinfo_for_class_or_defer(rel_pk_field.__class__)
            if rel_pk_field_info is None:
                continue

            field_type = fields.get_field_type(rel_pk_field_info,
                                               is_nullable=self.django_context.get_field_nullability(field))
            self.add_new_model_attribute(rel_pk_field_name, field_type)


class InjectAnyAsBaseForNestedMeta(TransformModelClassCallback):
    """
    Replaces
        class MyModel(models.Model):
            class Meta:
                pass
    with
        class MyModel(models.Model):
            class Meta(Any):
                pass
    to get around incompatible Meta inner classes for different models.
    """

    def modify_class_defn(self) -> None:
        meta_node = sem_helpers.get_nested_meta_node_for_current_class(self.class_defn.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddMetaOptionsAttribute(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        if '_meta' not in self.class_defn.info.names:
            options_info = self.lookup_typeinfo_or_defer(fullnames.OPTIONS_CLASS_FULLNAME)
            if options_info is not None:
                self.add_new_model_attribute('_meta',
                                             Instance(options_info, [
                                                 Instance(self.class_defn.info, [])
                                             ]))


class AddExtraFieldMethods(TransformModelClassCallback):
    def modify_model_class_defn(self, runtime_model_cls: Type[Model]) -> None:
        # get_FOO_display for choices
        for field in self.django_context.get_model_fields(runtime_model_cls):
            if field.choices:
                info = self.lookup_typeinfo_or_defer('builtins.str')
                assert info is not None
                return_type = Instance(info, [])
                common.add_method(self.ctx,
                                  name='get_{}_display'.format(field.attname),
                                  args=[],
                                  return_type=return_type)

        # get_next_by, get_previous_by for Date, DateTime
        for field in self.django_context.get_model_fields(runtime_model_cls):
            if isinstance(field, (DateField, DateTimeField)) and not field.null:
                return_type = Instance(self.class_defn.info, [])
                common.add_method(self.ctx,
                                  name='get_next_by_{}'.format(field.attname),
                                  args=[Argument(Var('kwargs', AnyType(TypeOfAny.explicit)),
                                                 AnyType(TypeOfAny.explicit),
                                                 initializer=None,
                                                 kind=ARG_STAR2)],
                                  return_type=return_type)
                common.add_method(self.ctx,
                                  name='get_previous_by_{}'.format(field.attname),
                                  args=[Argument(Var('kwargs', AnyType(TypeOfAny.explicit)),
                                                 AnyType(TypeOfAny.explicit),
                                                 initializer=None,
                                                 kind=ARG_STAR2)],
                                  return_type=return_type)


class ModelCallback(helpers.ClassDefPluginCallback):
    def __call__(self, ctx: ClassDefContext) -> None:
        callback_classes = [
            AddManagersCallback,
            AddPrimaryKeyIfDoesNotExist,
            AddForeignPrimaryKeys,
            AddDefaultManagerCallback,
            AddRelatedManagersCallback,
            InjectAnyAsBaseForNestedMeta,
            AddMetaOptionsAttribute,
            AddExtraFieldMethods,
        ]
        for callback_cls in callback_classes:
            callback = callback_cls(self.plugin)  # type: ignore
            callback.__call__(ctx)

    def modify_class_defn(self) -> None:
        raise NotImplementedError()
