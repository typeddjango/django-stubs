from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import AssignmentStmt, NameExpr, TypeInfo, Var
from mypy.types import Instance, get_proper_type

from mypy_django_plugin.lib import fullnames, helpers

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mypy.plugin import AttributeContext, ClassDefContext
    from mypy.types import Type as MypyType


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        if not ctx.api.final_iteration:
            ctx.api.defer()
    else:
        meta_node.fallback_to_any = True


def transform_form_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASEFORM_CLASS_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        bases = helpers.get_django_metadata_bases(sym.node, "baseform_bases")
        bases[ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)


def _iter_declared_field_names(info: TypeInfo) -> Iterator[str]:
    """Yield each class-body-assigned attribute name once, starts from the most-derived class."""
    seen: set[str] = set()
    for base_info in info.mro:
        for stmt in base_info.defn.defs.body:
            if isinstance(stmt, AssignmentStmt) and len(stmt.lvalues) == 1 and isinstance(stmt.lvalues[0], NameExpr):
                name = stmt.lvalues[0].name
                if name not in seen:
                    seen.add(name)
                    yield name


def transform_form_fields_attr_type(ctx: AttributeContext) -> MypyType:
    """Create type `form.fields` as a TypedDict of the form's declared fields, instead of `dict[str, Field]`."""
    if ctx.is_lvalue:
        return ctx.default_attr_type

    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_attr_type

    field_types: dict[str, MypyType] = {}
    for name in _iter_declared_field_names(object_type.type):
        symbol = object_type.type.get(name)
        if symbol is None or not isinstance(symbol.node, Var) or symbol.node.type is None:
            continue
        var_type = get_proper_type(symbol.node.type)
        if isinstance(var_type, Instance) and var_type.type.has_base(fullnames.FORM_FIELD_FULLNAME):
            field_types[name] = symbol.node.type

    if not field_types:
        return ctx.default_attr_type

    return helpers.make_typeddict(ctx.api, field_types)
