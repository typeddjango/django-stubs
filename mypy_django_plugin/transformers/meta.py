from mypy.plugin import MethodContext
from mypy.types import AnyType, Instance, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, get_field_type_from_model_type_info
from mypy_django_plugin.lib import helpers


def return_proper_field_type_from_get_field(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    # Options instance
    assert isinstance(ctx.type, Instance)

    # bail if list of generic params is empty
    if len(ctx.type.args) == 0:
        return ctx.default_return_type

    model_type = get_proper_type(ctx.type.args[0])
    if not isinstance(model_type, Instance):
        return ctx.default_return_type

    field_name_expr = helpers.get_call_argument_by_name(ctx, "field_name")
    if field_name_expr is None:
        return ctx.default_return_type

    field_name = helpers.resolve_string_attribute_value(field_name_expr, django_context)
    if field_name is None:
        return ctx.default_return_type

    field_type = get_field_type_from_model_type_info(model_type.type, field_name)
    if field_type is not None:
        return field_type

    ctx.api.fail(f"{model_type.type.name} has no field named {field_name!r}", ctx.context)
    return AnyType(TypeOfAny.from_error)
