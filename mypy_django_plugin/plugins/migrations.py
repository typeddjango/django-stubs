from typing import Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import Expression, StrExpr, TypeInfo
from mypy.plugin import MethodContext
from mypy.types import Instance, Type, TypeType

from mypy_django_plugin import helpers


def get_string_value_from_expr(expr: Expression) -> Optional[str]:
    if isinstance(expr, StrExpr):
        return expr.value
    # TODO: somehow figure out other cases
    return None


def determine_model_cls_from_string_for_migrations(ctx: MethodContext) -> Type:
    app_label_expr = ctx.args[ctx.callee_arg_names.index('app_label')][0]
    app_label = get_string_value_from_expr(app_label_expr)
    if app_label is None:
        return ctx.default_return_type

    if 'model_name' not in ctx.callee_arg_names:
        return ctx.default_return_type

    model_name_expr_tuple = ctx.args[ctx.callee_arg_names.index('model_name')]
    if not model_name_expr_tuple:
        return ctx.default_return_type

    model_name = get_string_value_from_expr(model_name_expr_tuple[0])
    if model_name is None:
        return ctx.default_return_type

    api = cast(TypeChecker, ctx.api)
    model_fullname = helpers.get_model_fullname(app_label, model_name, all_modules=api.modules)

    if model_fullname is None:
        return ctx.default_return_type
    model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                        all_modules=api.modules)
    if model_info is None or not isinstance(model_info, TypeInfo):
        return ctx.default_return_type
    return TypeType(Instance(model_info, []))
