import dataclasses
from abc import ABCMeta, abstractmethod
from typing import Optional, Type, cast

from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from mypy.newsemanal.semanal import NewSemanticAnalyzer
from mypy.nodes import ARG_NAMED_OPT, Argument, ClassDef, MDEF, SymbolTableNode, TypeInfo, Var
from mypy.plugin import ClassDefContext
from mypy.plugins import common
from mypy.types import AnyType, Instance, NoneType, Type as MypyType, UnionType

from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField, Field
from mypy_django_plugin_newsemanal.context import DjangoContext
from mypy_django_plugin_newsemanal.lib import helpers
from mypy_django_plugin_newsemanal.transformers import fields
from mypy_django_plugin_newsemanal.transformers.fields import get_field_descriptor_types


@dataclasses.dataclass
class ModelClassInitializer(metaclass=ABCMeta):
    api: NewSemanticAnalyzer
    model_classdef: ClassDef
    django_context: DjangoContext
    ctx: ClassDefContext

    @classmethod
    def from_ctx(cls, ctx: ClassDefContext, django_context: DjangoContext):
        return cls(api=cast(NewSemanticAnalyzer, ctx.api),
                   model_classdef=ctx.cls,
                   django_context=django_context,
                   ctx=ctx)

    def lookup_typeinfo_or_incomplete_defn_error(self, fullname: str) -> TypeInfo:
        sym = self.api.lookup_fully_qualified_or_none(fullname)
        if sym is None or not isinstance(sym.node, TypeInfo):
            raise helpers.IncompleteDefnException(f'No {fullname!r} found')
        return sym.node

    def lookup_field_typeinfo_or_incomplete_defn_error(self, field: Field) -> TypeInfo:
        fullname = helpers.get_class_fullname(field.__class__)
        field_info = self.lookup_typeinfo_or_incomplete_defn_error(fullname)
        return field_info

    def add_new_node_to_model_class(self, name: str, typ: Instance) -> None:
        # type=: type of the variable itself
        var = Var(name=name, type=typ)
        # var.info: type of the object variable is bound to
        var.info = self.model_classdef.info
        var._fullname = self.model_classdef.info.fullname() + '.' + name
        var.is_initialized_in_class = True
        var.is_inferred = True
        self.model_classdef.info.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True)
        # assert self.model_classdef.info == self.api.type
        # self.api.add_symbol_table_node(name, SymbolTableNode(MDEF, var, plugin_generated=True))

    def convert_any_to_type(self, typ: MypyType, referred_to_type: MypyType) -> MypyType:
        if isinstance(typ, UnionType):
            converted_items = []
            for item in typ.items:
                converted_items.append(self.convert_any_to_type(item, referred_to_type))
            return UnionType.make_union(converted_items,
                                        line=typ.line, column=typ.column)
        if isinstance(typ, Instance):
            args = []
            for default_arg in typ.args:
                if isinstance(default_arg, AnyType):
                    args.append(referred_to_type)
                else:
                    args.append(default_arg)
            return helpers.reparametrize_instance(typ, args)

        if isinstance(typ, AnyType):
            return referred_to_type

        return typ

    def get_field_set_type(self, field: Field, method: str) -> MypyType:
        target_field = field
        if isinstance(field, ForeignKey):
            target_field = field.target_field
        field_fullname = helpers.get_class_fullname(target_field.__class__)
        field_info = self.lookup_typeinfo_or_incomplete_defn_error(field_fullname)
        field_set_type = helpers.get_private_descriptor_type(field_info, '_pyi_private_set_type',
                                                             is_nullable=self.get_field_nullability(field, method))
        if isinstance(target_field, ArrayField):
            argument_field_type = self.get_field_set_type(target_field.base_field, method)
            field_set_type = self.convert_any_to_type(field_set_type, argument_field_type)
        return field_set_type

    def get_field_nullability(self, field: Field, method: Optional[str]) -> bool:
        nullable = field.null
        if not nullable and isinstance(field, CharField) and field.blank:
            return True
        if method == '__init__':
            if field.primary_key or isinstance(field, ForeignKey):
                return True
        return nullable

    def get_field_kind(self, field: Field, method: str):
        if method == '__init__':
            # all arguments are optional in __init__
            return ARG_NAMED_OPT

    def get_primary_key_field(self, model_cls: Type[Model]) -> Field:
        for field in model_cls._meta.get_fields():
            if isinstance(field, Field):
                if field.primary_key:
                    return field
        raise ValueError('No primary key defined')

    def make_field_kwarg(self, name: str, field: Field, method: str) -> Argument:
        field_set_type = self.get_field_set_type(field, method)
        kind = self.get_field_kind(field, method)
        field_kwarg = Argument(variable=Var(name, field_set_type),
                               type_annotation=field_set_type,
                               initializer=None,
                               kind=kind)
        return field_kwarg

    def get_field_kwargs(self, model_cls: Type[Model], method: str):
        field_kwargs = []
        if method == '__init__':
            # add primary key `pk`
            primary_key_field = self.get_primary_key_field(model_cls)
            field_kwarg = self.make_field_kwarg('pk', primary_key_field, method)
            field_kwargs.append(field_kwarg)

            for field in model_cls._meta.get_fields():
                if isinstance(field, Field):
                    field_kwarg = self.make_field_kwarg(field.attname, field, method)
                    field_kwargs.append(field_kwarg)

                    if isinstance(field, ForeignKey):
                        attname = field.name
                        related_model_fullname = helpers.get_class_fullname(field.related_model)
                        model_info = self.lookup_typeinfo_or_incomplete_defn_error(related_model_fullname)
                        is_nullable = self.get_field_nullability(field, method)
                        field_set_type = Instance(model_info, [])
                        if is_nullable:
                            field_set_type = helpers.make_optional(field_set_type)
                        kind = self.get_field_kind(field, method)
                        field_kwarg = Argument(variable=Var(attname, field_set_type),
                                               type_annotation=field_set_type,
                                               initializer=None,
                                               kind=kind)
                        field_kwargs.append(field_kwarg)
        return field_kwargs

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()


class InjectAnyAsBaseForNestedMeta(ModelClassInitializer):
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

    def run(self) -> None:
        meta_node = helpers.get_nested_meta_node_for_current_class(self.model_classdef.info)
        if meta_node is None:
            return None
        meta_node.fallback_to_any = True


class AddDefaultPrimaryKey(ModelClassInitializer):
    def run(self) -> None:
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.fullname)
        if model_cls is None:
            return

        auto_field = model_cls._meta.auto_field
        if auto_field and not self.model_classdef.info.has_readable_member(auto_field.attname):
            # autogenerated field
            auto_field_fullname = helpers.get_class_fullname(auto_field.__class__)
            auto_field_info = self.lookup_typeinfo_or_incomplete_defn_error(auto_field_fullname)

            set_type, get_type = fields.get_field_descriptor_types(auto_field_info, is_nullable=False)
            self.add_new_node_to_model_class(auto_field.attname, Instance(auto_field_info,
                                                                          [set_type, get_type]))


class AddRelatedModelsId(ModelClassInitializer):
    def run(self) -> None:
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.fullname)
        if model_cls is None:
            return

        for field in model_cls._meta.get_fields():
            if isinstance(field, ForeignKey):
                rel_primary_key_field = self.get_primary_key_field(field.related_model)
                field_info = self.lookup_field_typeinfo_or_incomplete_defn_error(rel_primary_key_field)
                is_nullable = self.get_field_nullability(field, None)
                set_type, get_type = get_field_descriptor_types(field_info, is_nullable)
                self.add_new_node_to_model_class(field.attname,
                                                 Instance(field_info, [set_type, get_type]))


class AddManagers(ModelClassInitializer):
    def run(self):
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.fullname)
        if model_cls is None:
            return

        for manager_name, manager in model_cls._meta.managers_map.items():
            if manager_name not in self.model_classdef.info.names:
                manager_fullname = helpers.get_class_fullname(manager.__class__)
                manager_info = self.lookup_typeinfo_or_incomplete_defn_error(manager_fullname)

                manager = Instance(manager_info, [Instance(self.model_classdef.info, [])])
                self.add_new_node_to_model_class(manager_name, manager)

        # add _default_manager
        if '_default_manager' not in self.model_classdef.info.names:
            default_manager_fullname = helpers.get_class_fullname(model_cls._meta.default_manager.__class__)
            default_manager_info = self.lookup_typeinfo_or_incomplete_defn_error(default_manager_fullname)
            default_manager = Instance(default_manager_info, [Instance(self.model_classdef.info, [])])
            self.add_new_node_to_model_class('_default_manager', default_manager)


class AddInitMethod(ModelClassInitializer):
    def run(self):
        model_cls = self.django_context.get_model_class_by_fullname(self.model_classdef.info.fullname())
        if model_cls is None:
            return

        field_kwargs = self.get_field_kwargs(model_cls, '__init__')
        common.add_method(self.ctx, '__init__', field_kwargs, NoneType())


def process_model_class(ctx: ClassDefContext,
                        django_context: DjangoContext) -> None:
    initializers = [
        InjectAnyAsBaseForNestedMeta,
        AddDefaultPrimaryKey,
        AddRelatedModelsId,
        AddManagers,
        AddInitMethod
    ]
    for initializer_cls in initializers:
        try:
            initializer_cls.from_ctx(ctx, django_context).run()
        except helpers.IncompleteDefnException:
            if not ctx.api.final_iteration:
                ctx.api.defer()