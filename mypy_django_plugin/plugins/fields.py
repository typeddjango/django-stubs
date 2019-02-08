from mypy.plugin import FunctionContext
from mypy.types import Type, Instance

from mypy_django_plugin import helpers


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    base_field_arg_type = helpers.get_argument_type_by_name(ctx, 'base_field')
    if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
        return ctx.default_return_type

    get_method = base_field_arg_type.type.get_method('__get__')
    if not get_method:
        # not a method
        return ctx.default_return_type

    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[get_method.type.ret_type])
