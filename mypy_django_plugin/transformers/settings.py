from mypy.nodes import MemberExpr
from mypy.plugin import AttributeContext
from mypy.types import AnyType, TypeOfAny
from mypy.types import Type as MypyType

from mypy_django_plugin.config import DjangoPluginConfig
from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def get_type_of_settings_attribute(
    ctx: AttributeContext, django_context: DjangoContext, plugin_config: DjangoPluginConfig
) -> MypyType:
    if not isinstance(ctx.context, MemberExpr):
        return ctx.default_attr_type

    setting_name = ctx.context.name

    typechecker_api = helpers.get_typechecker_api(ctx)

    # first look for the setting in the project settings file, then global settings
    settings_module = typechecker_api.modules.get(django_context.django_settings_module)
    global_settings_module = typechecker_api.modules.get("django.conf.global_settings")
    for module in [settings_module, global_settings_module]:
        if module is not None:
            sym = module.names.get(setting_name)
            if sym is not None:
                if sym.type is None:
                    # When analysing a function, mypy will defer analysis to a later pass
                    typechecker_api.handle_cannot_determine_type(setting_name, ctx.context)
                    return ctx.default_attr_type
                return sym.type

    # Now, we want to check if this setting really exist in runtime.
    # If it does, we just return `Any`, not to raise any false-positives.
    # But, we cannot reconstruct the exact runtime type.
    # See https://github.com/typeddjango/django-stubs/pull/1163
    if not plugin_config.strict_settings and hasattr(django_context.settings, setting_name):
        return AnyType(TypeOfAny.implementation_artifact)

    ctx.api.fail(f"'Settings' object has no attribute {setting_name!r}", ctx.context)
    return ctx.default_attr_type
