from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import ClassDef, RefExpr, TypeAlias, TypeInfo
from mypy.semanal_shared import has_placeholder
from mypy.types import Instance, get_proper_type

if TYPE_CHECKING:
    from mypy.plugin import ClassDefContext


def _omits_type_args(cls: ClassDef, parent: TypeInfo) -> bool:
    """Whether `cls` subclasses `parent` without type args, directly or through an alias like `QS = QuerySet`.

    Omitted args are indistinguishable from explicit ones once mypy has filled in the PEP 696 defaults,
    so this reads omission off the source: https://github.com/python/mypy/blob/v2.4.0/mypy/typeanal.py#L2180
    """
    for expr in cls.base_type_exprs:
        node = expr.node if isinstance(expr, RefExpr) else None
        if isinstance(node, TypeAlias) and node.no_args:
            target = get_proper_type(node.target)
            node = target.type if isinstance(target, Instance) else None
        if node is parent:
            return True
    return False


def reparametrize_generic_class(
    ctx: ClassDefContext,
    base_class_fullname: str,
    *,
    bind_explicit_args: bool = False,
) -> None:
    """
    Add implicit pass-through generics to subclasses of generic stub classes that omit their type arguments.

    Eg.

        class MyManager(models.Manager): ...

    is interpreted as:

        class MyManager(models.Manager[_T_co, _QS_co]): ...

    When ``bind_explicit_args`` is True, also reparametrize partially or
    fully-explicit parametrizations by binding each explicit arg as both
    the bound and the PEP 696 default of a synthesized covariant TypeVar.

    Note that this does not happen if mypy is run with disallow_any_generics = True,
    as not specifying the generic type is then considered an error.
    """
    if ctx.api.options.disallow_any_generics:
        # Let mypy's own "missing type arguments" error stand rather than silently reparametrize.
        return

    class_info = ctx.api.lookup_fully_qualified_or_none(ctx.cls.fullname)
    if class_info is None or class_info.node is None:
        return
    assert isinstance(class_info.node, TypeInfo)

    if class_info.node.type_vars:
        # We've already been here or the class is already declared with generic types
        return

    parent_class = next(
        (base for base in class_info.node.bases if base.type.has_base(base_class_fullname)),
        None,
    )
    if parent_class is None or not parent_class.args:
        return

    parent_info = parent_class.type
    if _omits_type_args(ctx.cls, parent_info):
        # Args were omitted -- reuse the parent's TypeVars so their existing
        # PEP 696 defaults (e.g. `_Row_co = TypeVar(default=_Model_co)`) are preserved.
        type_vars = list(parent_info.defn.type_vars)
    elif bind_explicit_args and parent_info.fullname == base_class_fullname:
        # Args were supplied explicitly on the canonical base class -- synthesize TypeVars bounded by
        # the user's args so the subclass stays effectively concrete in user-facing contexts
        # (defaults + bound + covariance) while still being generic enough for the plugin
        # to flow annotation row types through.
        type_vars = [
            type_var.copy_modified(id=type_var.id, upper_bound=arg, default=arg)
            for type_var, arg in zip(parent_info.defn.type_vars, parent_class.args, strict=True)
        ]
    else:
        # Explicit args elsewhere (e.g. `Manager[Book]`, `TextField[str, str]`) are left as written.
        return

    # If we end up with placeholders we need to defer so the placeholders are
    # resolved in a future iteration
    if any(has_placeholder(type_var) for type_var in type_vars):
        if not ctx.api.final_iteration:
            ctx.api.defer()
        else:
            return

    parent_class.args = tuple(type_vars)
    class_info.node.defn.type_vars = type_vars
    class_info.node.add_type_vars()
