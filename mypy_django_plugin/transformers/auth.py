from mypy.nodes import TypeInfo
from mypy.plugin import AnalyzeTypeContext
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import TypeAnalyser
from mypy.types import PlaceholderType, ProperType
from mypy.types import Type as MypyType
from mypy.typevars import fill_typevars_with_any

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


def get_user_model(ctx: AnalyzeTypeContext, django_context: DjangoContext) -> MypyType:
    assert isinstance(ctx.api, TypeAnalyser)
    assert isinstance(ctx.api.api, SemanticAnalyzer)

    def get_abstract_base_user(api: SemanticAnalyzer) -> ProperType:
        sym = api.lookup_fully_qualified(fullnames.ABSTRACT_BASE_USER_MODEL_FULLNAME)
        assert isinstance(sym.node, TypeInfo)
        return fill_typevars_with_any(sym.node)

    if not django_context.is_contrib_auth_installed:
        return get_abstract_base_user(ctx.api.api)

    auth_user_model = django_context.settings.AUTH_USER_MODEL
    model_info = helpers.resolve_lazy_reference(
        auth_user_model, api=ctx.api.api, django_context=django_context, ctx=ctx.context
    )
    if model_info is None:
        fullname = django_context.model_class_fullnames_by_label.get(auth_user_model)
        if fullname is not None:
            # When we've tried to resolve 'AUTH_USER_MODEL' but got no class back but
            # we notice that its value is recognised we'll return a placeholder for
            # the class as we expect it to exist later on.
            return PlaceholderType(fullname=fullname, args=[], line=ctx.context.line)
        return get_abstract_base_user(ctx.api.api)

    return fill_typevars_with_any(model_info)
