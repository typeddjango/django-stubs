from typing import Optional, Callable, cast

from mypy.checker import TypeChecker
from mypy.nodes import Var, MDEF, SymbolTableNode
from mypy.plugin import Plugin, FunctionContext
from mypy.types import Type, CallableType, Instance


def extract_to_value_type(ctx: FunctionContext) -> Optional[Type]:
    assert 'to' in ctx.context.arg_names
    to_arg_value = ctx.arg_types[ctx.context.arg_names.index('to')][0]
    if not isinstance(to_arg_value, CallableType):
        return None

    return to_arg_value.ret_type


def extract_related_name_value(ctx: FunctionContext) -> str:
    return ctx.context.args[ctx.context.arg_names.index('related_name')].value


def set_related_name_manager_for_foreign_key(ctx: FunctionContext) -> Type:
    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    referred_to = extract_to_value_type(ctx)
    if not referred_to:
        return ctx.default_return_type

    related_name = extract_related_name_value(ctx)
    outer_class_info = ctx.api.tscope.classes[-1]

    queryset_type = ctx.api.named_generic_type('django.db.models.QuerySet',
                                               args=[Instance(outer_class_info, [])])
    related_var = Var(related_name,
                      queryset_type)
    related_var.info = queryset_type.type
    referred_to.type.names[related_name] = SymbolTableNode(MDEF, related_var,
                                                           plugin_generated=True)
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
    related_instance_type = api.named_type(outer_class_info.fullname())
    related_var = Var(related_name, related_instance_type)
    related_var.info = related_instance_type.type

    referred_to.type.names[related_name] = SymbolTableNode(MDEF, related_var,
                                                           plugin_generated=True)
    return ctx.default_return_type


class RelatedFieldsPlugin(Plugin):
    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.db.models.fields.related.ForeignKey':
            return set_related_name_manager_for_foreign_key

        if fullname == 'django.db.models.fields.related.OneToOneField':
            return set_related_name_instance_for_onetoonefield

        return None


def plugin(version):
    return RelatedFieldsPlugin
