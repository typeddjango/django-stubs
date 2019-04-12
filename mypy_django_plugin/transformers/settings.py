from typing import TYPE_CHECKING, List, Optional, cast

from mypy.checkexpr import FunctionContext
from mypy.checkmember import AttributeContext
from mypy.nodes import NameExpr, StrExpr, SymbolTableNode, TypeInfo
from mypy.types import AnyType, Instance, Type, TypeOfAny, TypeType

from mypy_django_plugin import helpers

if TYPE_CHECKING:
    from mypy.checker import TypeChecker


def get_setting_sym(name: str, api: 'TypeChecker', settings_modules: List[str]) -> Optional[SymbolTableNode]:
    for settings_mod_name in settings_modules:
        if settings_mod_name not in api.modules:
            continue

        file = api.modules[settings_mod_name]
        sym = file.names.get(name)
        if sym is not None:
            return sym

    return None


def get_type_of_setting(ctx: AttributeContext, setting_name: str,
                        settings_modules: List[str], ignore_missing_settings: bool) -> Type:
    setting_sym = get_setting_sym(setting_name, ctx.api, settings_modules)
    if setting_sym:
        if setting_sym.type is None:
            # TODO: defer till setting_sym.type is not None
            return AnyType(TypeOfAny.implementation_artifact)

        return setting_sym.type

    if not ignore_missing_settings:
        ctx.api.fail(f"'Settings' object has no attribute {setting_name!r}", ctx.context)

    return ctx.default_attr_type


def return_user_model_hook(ctx: FunctionContext, settings_modules: List[str]) -> Type:
    from mypy.checker import TypeChecker

    api = cast(TypeChecker, ctx.api)

    setting_sym = get_setting_sym('AUTH_USER_MODEL', api, settings_modules)
    if setting_sym is None:
        return ctx.default_return_type

    setting_module_name, _, _ = setting_sym.fullname.rpartition('.')
    setting_module = api.modules[setting_module_name]

    model_path = None
    for name_expr, rvalue_expr in helpers.iter_over_assignments(setting_module):
        if isinstance(name_expr, NameExpr) and isinstance(rvalue_expr, StrExpr):
            if name_expr.name == 'AUTH_USER_MODEL':
                model_path = rvalue_expr.value
                break

    if not model_path:
        return ctx.default_return_type

    app_label, _, model_class_name = model_path.rpartition('.')
    if app_label is None:
        return ctx.default_return_type

    model_fullname = helpers.get_model_fullname(app_label, model_class_name,
                                                all_modules=api.modules)
    if model_fullname is None:
        api.fail(f'"{app_label}.{model_class_name}" model class is not imported so far. Try to import it '
                 f'(under if TYPE_CHECKING) at the beginning of the current file',
                 context=ctx.context)
        return ctx.default_return_type

    model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                        all_modules=api.modules)
    if model_info is None or not isinstance(model_info, TypeInfo):
        return ctx.default_return_type
    return TypeType(Instance(model_info, []))
