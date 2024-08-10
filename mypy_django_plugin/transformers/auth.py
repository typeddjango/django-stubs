from mypy.plugin import FunctionContext
from mypy.types import NoneType, UnionType
from mypy.types import Type as MypyType
from mypy.typevars import fill_typevars_with_any

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def update_authenticate_hook(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    if not django_context.is_contrib_auth_installed:
        return ctx.default_return_type

    auth_user_model = django_context.settings.AUTH_USER_MODEL
    api = helpers.get_typechecker_api(ctx)
    model_info = helpers.resolve_lazy_reference(
        auth_user_model, api=api, django_context=django_context, ctx=ctx.context
    )
    if model_info is None:
        return ctx.default_return_type

    return UnionType([fill_typevars_with_any(model_info), NoneType()], ctx.context.line, ctx.context.column)
