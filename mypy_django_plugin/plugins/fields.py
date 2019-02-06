from mypy.plugin import FunctionContext
from mypy.types import Type, Instance


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    if 'base_field' not in ctx.callee_arg_names:
        return ctx.default_return_type

    base_field_arg_type = ctx.arg_types[ctx.callee_arg_names.index('base_field')][0]
    if not isinstance(base_field_arg_type, Instance):
        return ctx.default_return_type

    get_method = base_field_arg_type.type.get_method('__get__')
    if not get_method:
        # not a method
        return ctx.default_return_type

    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[get_method.type.ret_type])
