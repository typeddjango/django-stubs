from typing import Optional

from mypy.nodes import StrExpr, TypeInfo
from mypy.plugin import MethodContext
from mypy.types import Instance, TypeType
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def resolve_model_for_get_model(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Attempts to refine the return type of an 'apps.get_model()' call
    """
    if not ctx.args:
        return ctx.default_return_type

    model_info: Optional[TypeInfo] = None
    # An 'apps.get_model("...")' call
    if ctx.args[0] and not ctx.args[1]:
        expr = ctx.args[0][0]
        if isinstance(expr, StrExpr):
            model_info = helpers.resolve_lazy_reference(
                expr.value, api=helpers.get_typechecker_api(ctx), django_context=django_context, ctx=expr
            )
    # An 'apps.get_model("...", "...")' call
    elif ctx.args[0] and ctx.args[1]:
        app_label = ctx.args[0][0]
        model_name = ctx.args[1][0]
        if isinstance(app_label, StrExpr) and isinstance(model_name, StrExpr):
            model_info = helpers.resolve_lazy_reference(
                f"{app_label.value}.{model_name.value}",
                api=helpers.get_typechecker_api(ctx),
                django_context=django_context,
                ctx=model_name,
            )

    if model_info is None:
        return ctx.default_return_type
    return TypeType(Instance(model_info, []))
