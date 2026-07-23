from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import StrExpr
from mypy.types import Instance, TypeType
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import helpers

if TYPE_CHECKING:
    from mypy.plugin import MethodContext

    from mypy_django_plugin.django.context import DjangoContext


def _get_model_lazy_reference(ctx: MethodContext) -> str | None:
    """Resolve a `get_model` call to a `<app_label>.<model_name>` lazy reference."""
    app_label = helpers.get_call_argument_by_name(ctx, "app_label")
    model_name = helpers.get_call_argument_by_name(ctx, "model_name")

    if not isinstance(app_label, StrExpr):
        return None

    if model_name is None:
        # Shortcut form: `app_label` is already "<app_label>.<model_name>".
        return app_label.value

    if isinstance(model_name, StrExpr):
        return f"{app_label.value}.{model_name.value}"

    return None


def resolve_model_for_get_model(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """Narrow the return type of an `apps.get_model()` call to the referenced model.

        apps.get_model("myapp.MyModel")        # -> type[myapp.models.MyModel]
        apps.get_model("myapp", "MyModel")      # -> type[myapp.models.MyModel]

    The model name is case-insensitive, so `"myapp.mymodel"` resolves too.

    Non-literal arguments keep the permissive `type[Any]` fallback:

        apps.get_model(app_label, model_name)   # -> type[Any]
    """
    if (lazy_reference := _get_model_lazy_reference(ctx)) and (
        model_info := helpers.resolve_lazy_reference(
            lazy_reference,
            api=helpers.get_typechecker_api(ctx),
            django_context=django_context,
            ctx=ctx.context,
        )
    ):
        return TypeType(Instance(model_info, []))
    return ctx.default_return_type
