"""App registry"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import StrExpr
from mypy.types import Type as MypyType
from mypy.types import TypeType

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
    """Narrow `apps.get_model()` to the referenced model

    With literal arguments, the model class is returned instead of `type[Any]`.

    ```python
    reveal_type(apps.get_model("myapp.Book"))  # type[Book]
    apps.get_model("myapp.Missing")  # error: Could not match lazy reference with any model  [misc]
    ```

    Migration `apps` (`StateApps`) keep `type[Any]`, since their models are historical.
    """
    if (lazy_reference := _get_model_lazy_reference(ctx)) and (
        model_info := helpers.resolve_lazy_reference(
            lazy_reference,
            api=helpers.get_typechecker_api(ctx),
            django_context=django_context,
            ctx=ctx.context,
        )
    ):
        return TypeType(helpers.model_instance(model_info))
    return ctx.default_return_type
