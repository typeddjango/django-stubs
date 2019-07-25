from mypy.plugin import AttributeContext
from mypy.types import Instance
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def set_auth_user_model_as_type_for_request_user(ctx: AttributeContext, django_context: DjangoContext) -> MypyType:
    auth_user_model = django_context.settings.AUTH_USER_MODEL
    model_cls = django_context.apps_registry.get_model(auth_user_model)
    model_info = helpers.lookup_class_typeinfo(helpers.get_typechecker_api(ctx), model_cls)
    if model_info is None:
        return ctx.default_attr_type

    return Instance(model_info, [])
