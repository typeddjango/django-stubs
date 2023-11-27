from mypy.plugin import FunctionSigContext
from mypy.types import CallableType, FunctionLike, Instance, UnionType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def transform_user_passes_test(ctx: FunctionSigContext, django_context: DjangoContext) -> FunctionLike:
    """
    Update the signature of user_passes_test to reflect settings.AUTH_USER_MODEL
    """

    auth_user_model = django_context.settings.AUTH_USER_MODEL
    try:
        model_cls = django_context.apps_registry.get_model(auth_user_model)
    except LookupError:
        return ctx.default_signature
    model_cls_fullname = helpers.get_class_fullname(model_cls)
    user_model_info = helpers.lookup_fully_qualified_typeinfo(helpers.get_typechecker_api(ctx), model_cls_fullname)
    if user_model_info is None:
        return ctx.default_signature

    if not ctx.default_signature.arg_types or not isinstance(ctx.default_signature.arg_types[0], CallableType):
        return ctx.default_signature

    test_func_type = ctx.default_signature.arg_types[0]

    if not test_func_type.arg_types or not isinstance(test_func_type.arg_types[0], UnionType):
        return ctx.default_signature
    union = test_func_type.arg_types[0]

    new_union = UnionType([Instance(user_model_info, [])] + union.items[1:])

    new_test_func_type = test_func_type.copy_modified(
        arg_types=[new_union] + test_func_type.arg_types[1:],
    )

    return ctx.default_signature.copy_modified(
        arg_types=[new_test_func_type] + ctx.default_signature.arg_types[1:],
    )
