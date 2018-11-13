from mypy.plugin import FunctionContext
from mypy.types import Type

from mypy_django_plugin import helpers


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    signature = helpers.get_call_signature_or_none(ctx)
    if signature is None:
        return ctx.default_return_type

    _, base_field_arg_type = signature['base_field']
    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[base_field_arg_type.type.names['__get__'].type.ret_type])
