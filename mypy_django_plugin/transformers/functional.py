from mypy.errorcodes import ATTR_DEFINED
from mypy.nodes import CallExpr, MemberExpr
from mypy.plugin import AttributeContext
from mypy.types import AnyType, CallableType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.lib import helpers


def resolve_str_promise_attribute(ctx: AttributeContext) -> MypyType:
    if isinstance(ctx.context, MemberExpr):
        method_name = ctx.context.name
    elif isinstance(ctx.context, CallExpr) and isinstance(ctx.context.callee, MemberExpr):
        method_name = ctx.context.callee.name
    else:
        ctx.api.fail(f'Cannot resolve the attribute of "{ctx.type}"', ctx.context, code=ATTR_DEFINED)
        return AnyType(TypeOfAny.from_error)

    str_info = helpers.lookup_fully_qualified_typeinfo(helpers.get_typechecker_api(ctx), f"builtins.str")
    assert str_info is not None
    method = str_info.get(method_name)

    if method is None or method.type is None:
        ctx.api.fail(f'"{ctx.type}" has no attribute "{method_name}"', ctx.context, code=ATTR_DEFINED)
        return AnyType(TypeOfAny.from_error)

    if isinstance(method.type, CallableType):
        # The proxied str methods are only meant to be used as instance methods.
        # We need to drop the first `self` argument in them.
        assert method.type.arg_names[0] == "self"
        return method.type.copy_modified(
            arg_kinds=method.type.arg_kinds[1:],
            arg_names=method.type.arg_names[1:],
            arg_types=method.type.arg_types[1:],
        )
    else:
        # Not possible with `builtins.str`, but we have error handling for this anyway.
        ctx.api.fail(f'"{method_name}" on "{ctx.type}" is not a method', ctx.context)
        return AnyType(TypeOfAny.from_error)
