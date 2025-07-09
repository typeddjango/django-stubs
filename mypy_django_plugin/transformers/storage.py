from mypy.checker import TypeChecker
from mypy.plugin import AnalyzeTypeContext, MethodContext
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import TypeAnalyser
from mypy.types import Instance, PlaceholderType, UninhabitedType, get_proper_type
from mypy.types import Type as MypyType
from mypy.typevars import fill_typevars

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def get_storage_backend(alias: str, django_context: DjangoContext) -> str | None:
    "Defensively look for a settings.STORAGES by its alias."

    try:
        fullname = django_context.settings.STORAGES[alias]["BACKEND"]
        if not isinstance(fullname, str) or "." not in fullname:
            return None

        return fullname
    except (KeyError, TypeError):
        return None


def get_storage(ctx: AnalyzeTypeContext, alias: str, django_context: DjangoContext) -> MypyType:
    """
    Get a storage type by its alias, but do not fail if it cannot be found since this is resolving an internal type-var,
    and errors would be reported in the type stubs.
    """

    assert isinstance(ctx.api, TypeAnalyser)
    assert isinstance(ctx.api.api, SemanticAnalyzer)

    if fullname := get_storage_backend(alias, django_context):
        if type_info := helpers.lookup_fully_qualified_typeinfo(ctx.api.api, fullname):
            return fill_typevars(type_info)

        if not ctx.api.api.final_iteration:
            ctx.api.api.defer()
            return PlaceholderType(fullname=fullname, args=[], line=ctx.context.line)

    return ctx.type


def extract_proper_type_for_getitem(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Provide type information for `StorageHandler.__getitem__` when providing a literal value.
    """

    assert isinstance(ctx.api, TypeChecker)

    if ctx.arg_types:
        alias_type = get_proper_type(ctx.arg_types[0][0])

        if (
            isinstance(alias_type, Instance)
            and (alias_literal := alias_type.last_known_value)
            and isinstance(alias := alias_literal.value, str)
        ):
            if alias not in django_context.settings.STORAGES:
                ctx.api.fail(f'Could not find config for "{alias}" in settings.STORAGES.', ctx.context)

            elif fullname := get_storage_backend(alias, django_context):
                type_info = helpers.lookup_fully_qualified_typeinfo(ctx.api, fullname)
                assert type_info
                return fill_typevars(type_info)

            else:
                ctx.api.fail(f'"{alias}" in settings.STORAGES is improperly configured.', ctx.context)

            return UninhabitedType()

    return ctx.default_return_type
