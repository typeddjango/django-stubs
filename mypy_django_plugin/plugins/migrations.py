from typing import cast

from mypy.checker import TypeChecker
from mypy.nodes import TypeInfo
from mypy.plugin import MethodContext
from mypy.types import Type, Instance, TypeType

from mypy_django_plugin import helpers


def determine_model_cls_from_string_for_migrations(ctx: MethodContext) -> Type:
    app_label = ctx.args[ctx.callee_arg_names.index('app_label')][0].value
    model_name = ctx.args[ctx.callee_arg_names.index('model_name')][0].value

    api = cast(TypeChecker, ctx.api)
    model_fullname = helpers.get_model_fullname(app_label, model_name, all_modules=api.modules)

    if model_fullname is None:
        return ctx.default_return_type
    model_info = helpers.lookup_fully_qualified_generic(model_fullname,
                                                        all_modules=api.modules)
    if model_info is None or not isinstance(model_info, TypeInfo):
        return ctx.default_return_type
    return TypeType(Instance(model_info, []))
