from typing import Optional, Callable

from mypy.nodes import SymbolTableNode, MDEF, Var
from mypy.plugin import Plugin, FunctionContext
from mypy.types import Type, CallableType, TypeOfAny, AnyType, Instance


def set_related_fields(ctx: FunctionContext) -> Type:
    if 'related_name' not in ctx.context.arg_names:
        return ctx.default_return_type

    assert 'to' in ctx.context.arg_names
    to_arg_value = ctx.arg_types[ctx.context.arg_names.index('to')][0]
    if not isinstance(to_arg_value, CallableType):
        return ctx.default_return_type

    referred_to = to_arg_value.ret_type
    related_name = ctx.context.args[ctx.context.arg_names.index('related_name')].value
    outer_class_info = ctx.api.tscope.classes[-1]

    queryset_type = ctx.api.named_generic_type('django.db.models.QuerySet',
                                               args=[Instance(outer_class_info, [])])
    related_var = Var(related_name,
                      queryset_type)
    related_var.info = queryset_type.type

    referred_to.type.names[related_name] = SymbolTableNode(MDEF, related_var)
    return ctx.default_return_type


class RelatedFieldsPlugin(Plugin):
    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        if fullname == 'django.db.models.fields.related.ForeignKey':
            return set_related_fields
        return None


def plugin(version):
    return RelatedFieldsPlugin
