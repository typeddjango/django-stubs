from django.core.exceptions import FieldDoesNotExist
from mypy.plugin import MethodContext
from mypy.types import AnyType, Instance, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, get_field_type_from_model_type_info
from mypy_django_plugin.lib import helpers
from mypy_django_plugin.lib.helpers import DjangoModel


def return_proper_field_type_from_get_field(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    if not (
        isinstance(ctx.type, Instance)
        and ctx.type.args
        and isinstance(model_type := get_proper_type(ctx.type.args[0]), Instance)
        and (field_name_expr := helpers.get_call_argument_by_name(ctx, "field_name")) is not None
        and (field_name := helpers.resolve_string_attribute_value(field_name_expr, django_context)) is not None
    ):
        return ctx.default_return_type

    field_type = get_field_type_from_model_type_info(model_type.type, field_name)
    if field_type is not None:
        return field_type

    if (django_model := DjangoModel.from_model_type(model_type, django_context)) is None:
        return ctx.default_return_type

    try:
        field = django_model.cls._meta.get_field(field_name)
        if field_info := helpers.lookup_class_typeinfo(helpers.get_typechecker_api(ctx), field.__class__):
            return Instance(field_info, [])
    except FieldDoesNotExist as e:
        ctx.api.fail(str(e), ctx.context)
        return AnyType(TypeOfAny.from_error)

    return ctx.default_return_type
