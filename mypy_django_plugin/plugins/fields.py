from mypy.plugin import FunctionContext
from mypy.types import Type


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    if 'base_field' not in ctx.callee_arg_names:
        return ctx.default_return_type

    base_field_arg_type = ctx.arg_types[ctx.callee_arg_names.index('base_field')][0]
    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[base_field_arg_type.type.names['__get__'].type.ret_type])
