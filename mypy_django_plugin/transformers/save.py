from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import ListExpr, SetExpr, TupleExpr
from mypy.types import Instance
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import helpers
from mypy_django_plugin.lib.field_validation import validate_non_pk_concrete_field

if TYPE_CHECKING:
    from mypy.plugin import MethodContext

    from mypy_django_plugin.django.context import DjangoContext


def validate_save_update_fields(ctx: MethodContext, django_context: DjangoContext, method: str) -> MypyType:
    """
    Type check the keyword-only `update_fields` argument passed to `Model.save(...)` / `Model.asave(...)`.
    """
    if not isinstance(ctx.type, Instance) or not helpers.is_model_type(ctx.type.type):
        return ctx.default_return_type
    django_model = helpers.DjangoModel.from_model_type(ctx.type, django_context)
    if django_model is None:
        return ctx.default_return_type

    update_fields_expr = helpers.get_call_argument_by_name(ctx, "update_fields")
    if not isinstance(update_fields_expr, (ListExpr, TupleExpr, SetExpr)):
        # `None`, a `set()` call, or any non-literal collection cannot be checked statically.
        return ctx.default_return_type

    for field_arg in update_fields_expr.items:
        field_name = helpers.resolve_string_attribute_value(field_arg, django_context)
        if field_name is not None:
            validate_non_pk_concrete_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type
