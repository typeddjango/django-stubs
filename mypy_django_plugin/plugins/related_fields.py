from typing import Optional, Callable, cast

from mypy.checker import TypeChecker
from mypy.nodes import Var, MDEF, SymbolTableNode, TypeInfo, SymbolTable
from mypy.plugin import Plugin, FunctionContext, ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2
from mypy.types import Type, CallableType, Instance

FOREIGN_KEY_FULLNAME = 'django.db.models.fields.related.ForeignKey'
ONETOONE_FIELD_FULLNAME = 'django.db.models.fields.related.OneToOneField'


def extract_to_value_type(ctx: FunctionContext) -> Optional[Instance]:
    assert 'to' in ctx.context.arg_names
    to_arg_value = ctx.arg_types[ctx.context.arg_names.index('to')][0]
    if not isinstance(to_arg_value, CallableType):
        return None

    return to_arg_value.ret_type


def extract_related_name_value(ctx: FunctionContext) -> str:
    return ctx.context.args[ctx.context.arg_names.index('related_name')].value


def create_new_symtable_node_for_class_member(name: str, instance: Instance) -> SymbolTableNode:
    new_var = Var(name, instance)
    new_var.info = instance.type

    return SymbolTableNode(MDEF, new_var, plugin_generated=True)


def add_new_class_member(klass_typeinfo: TypeInfo, name: str, new_member_instance: Instance) -> None:
    klass_typeinfo.names[name] = create_new_symtable_node_for_class_member(name,
                                                                           instance=new_member_instance)


def set_related_name_manager_for_foreign_key(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    outer_class_info = api.tscope.classes[-1]

    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    referred_to = extract_to_value_type(ctx)
    if not referred_to:
        return ctx.default_return_type

    related_name = extract_related_name_value(ctx)
    queryset_type = api.named_generic_type('django.db.models.QuerySet',
                                           args=[Instance(outer_class_info, [])])
    add_new_class_member(referred_to.type,
                         related_name, queryset_type)
    return ctx.default_return_type


def set_related_name_instance_for_onetoonefield(ctx: FunctionContext) -> Type:
    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    referred_to = extract_to_value_type(ctx)
    if referred_to is None:
        return ctx.default_return_type

    related_name = extract_related_name_value(ctx)
    outer_class_info = ctx.api.tscope.classes[-1]

    api = cast(TypeChecker, ctx.api)
    add_new_class_member(referred_to.type, related_name,
                         new_member_instance=api.named_type(outer_class_info.fullname()))
    return ctx.default_return_type


def set_fieldname_attrs_for_related_fields(ctx: ClassDefContext) -> None:
    api = ctx.api

    new_symtable_nodes = SymbolTable()
    for (name, symtable_node), assignment_stmt in zip(ctx.cls.info.names.items(), ctx.cls.defs.body):
        rvalue_callee = assignment_stmt.rvalue.callee
        if rvalue_callee.fullname in {FOREIGN_KEY_FULLNAME, ONETOONE_FIELD_FULLNAME}:
            name += '_id'
            new_node = create_new_symtable_node_for_class_member(name,
                                                                 instance=api.named_type('__builtins__.int'))
            new_symtable_nodes[name] = new_node

    for name, node in new_symtable_nodes.items():
        ctx.cls.info.names[name] = node


class RelatedFieldsPlugin(Plugin):
    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.db.models.fields.related.ForeignKey':
            return set_related_name_manager_for_foreign_key

        if fullname == 'django.db.models.fields.related.OneToOneField':
            return set_related_name_instance_for_onetoonefield

        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == 'django.db.models.base.Model':
            return set_fieldname_attrs_for_related_fields
        return None


def plugin(version):
    return RelatedFieldsPlugin
