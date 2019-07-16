from mypy.nodes import TypeInfo
from mypy.plugin import FunctionContext
from mypy.types import Type as MypyType, TypeType, Instance

from mypy_django_plugin_newsemanal.django.context import DjangoContext
from mypy_django_plugin_newsemanal.lib import helpers


def get_user_model_hook(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    auth_user_model = django_context.settings.AUTH_USER_MODEL
    model_cls = django_context.apps_registry.get_model(auth_user_model)
    model_cls_fullname = helpers.get_class_fullname(model_cls)

    model_info = helpers.lookup_fully_qualified_generic(model_cls_fullname, ctx.api.modules)
    assert isinstance(model_info, TypeInfo)

    return TypeType(Instance(model_info, []))

