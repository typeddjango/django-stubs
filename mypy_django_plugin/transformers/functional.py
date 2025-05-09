from typing import Any

from mypy.checkmember import analyze_member_access
from mypy.errorcodes import ATTR_DEFINED
from mypy.nodes import CallExpr, MemberExpr
from mypy.plugin import AttributeContext
from mypy.types import AnyType, Instance, TypeOfAny
from mypy.types import Type as MypyType
from mypy.version import __version__ as mypy_version

from mypy_django_plugin.lib import helpers

mypy_version_info = tuple(map(int, mypy_version.partition("+")[0].split(".")))


def resolve_str_promise_attribute(ctx: AttributeContext) -> MypyType:
    if isinstance(ctx.context, MemberExpr):
        method_name = ctx.context.name
    elif isinstance(ctx.context, CallExpr) and isinstance(ctx.context.callee, MemberExpr):
        method_name = ctx.context.callee.name
    else:
        ctx.api.fail(f'Cannot resolve the attribute of "{ctx.type}"', ctx.context, code=ATTR_DEFINED)
        return AnyType(TypeOfAny.from_error)

    str_info = helpers.lookup_fully_qualified_typeinfo(helpers.get_typechecker_api(ctx), "builtins.str")
    assert str_info is not None
    str_type = Instance(str_info, [])

    # TODO: [mypy 1.16+] Remove this workaround for passing `msg` to `analyze_member_access()`.
    extra: dict[str, Any] = {}
    if mypy_version_info < (1, 16):
        extra["msg"] = ctx.api.msg

    return analyze_member_access(
        method_name,
        str_type,
        ctx.context,
        is_lvalue=False,
        is_super=False,
        # operators are already handled with magic methods defined in the stubs for _StrPromise
        is_operator=False,
        original_type=ctx.type,
        chk=helpers.get_typechecker_api(ctx),
        **extra,
    )
