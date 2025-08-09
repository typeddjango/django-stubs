from mypy.nodes import MemberExpr, NameExpr, SuperExpr, TypeAlias, TypeInfo, Var
from mypy.plugin import AttributeContext
from mypy.typeanal import make_optional_type
from mypy.types import (
    AnyType,
    Instance,
    LiteralType,
    Overloaded,
    ProperType,
    TupleType,
    TypeOfAny,
    TypeType,
    TypeVarType,
    UnionType,
    get_proper_type,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import fullnames


# TODO: [mypy 1.14+] Remove this backport of `TypeInfo.enum_members`.
def _get_enum_members(info: TypeInfo) -> list[str]:
    try:
        return info.enum_members
    except AttributeError:  # mypy < 1.14
        pass

    return [
        name
        for name, sym in info.names.items()
        if (
            isinstance(sym.node, Var)
            and name not in ("_ignore_", "_order_", "__order__")
            and not name.startswith("__")
            and sym.node.has_explicit_value
        )
    ]


def _has_lazy_label(node: TypeInfo) -> bool:
    """
    Check whether a choices type has any lazy strings for labels.

    This is used to determine choices types that do not use lazy strings for labels such that a
    more simple type can be used instead of the default in the stubs.
    """
    assert node.is_enum

    if (sym := node.get("__empty__")) is not None:
        _empty_type = get_proper_type(sym.type)
        if isinstance(_empty_type, Instance) and _empty_type.type.has_base(fullnames.STR_PROMISE_FULLNAME):
            # If the empty label is lazy, then we don't need to check all the members.
            return True

    # TODO: [mypy 1.14+] Use `node.enum_members` and remove `_get_enum_members()` backport.
    for member_name in _get_enum_members(node):
        if (sym := node.get(member_name)) is None:
            continue

        _member_type = get_proper_type(sym.type)
        if not isinstance(_member_type, TupleType):
            # Member has auto-generated plain string label - enum.auto() or no explicit label.
            continue

        if _member_type.length() < 2:
            # There need to be at least two items in the tuple.
            continue

        _label_type = get_proper_type(_member_type.items[-1])
        if isinstance(_label_type, Instance) and _label_type.type.has_base(fullnames.STR_PROMISE_FULLNAME):
            # If any member label is lazy, then we don't need to check the remaining members.
            return True

    return False


def _try_replace_label(typ: ProperType, has_lazy_label: bool) -> MypyType:
    """
    Attempt to replace a label with a modified version.

    If there are no lazy strings for labels, remove the lazy string type.
    """
    if has_lazy_label:
        return typ

    if not isinstance(typ, UnionType):
        # If it's not a union, then it already is likely just `str` and not lazy.
        return typ

    items = [
        t
        for t in map(get_proper_type, typ.items)
        if isinstance(t, Instance) and not t.type.has_base(fullnames.STR_PROMISE_FULLNAME)
    ]

    # If we only have one item use that, otherwise make a new union.
    return UnionType.make_union(items) if len(items) > 1 else items[0]


def _try_replace_value(typ: ProperType, base_type: Instance | None, has_empty_label: bool) -> MypyType:
    """
    Attempt to replace a label with a modified version.

    If the value is of any type, then attempt to use the base type of the choices type.

    If the choices type has `__empty__` defined, then make the value type optional.
    """
    has_unknown_base = isinstance(typ, AnyType)

    if has_empty_label and has_unknown_base and base_type is not None:
        return make_optional_type(base_type)

    if has_empty_label:
        return make_optional_type(typ)

    if has_unknown_base and base_type is not None:
        return base_type

    return typ


def _get_enum_type_from_union_of_literals(typ: UnionType) -> MypyType:
    """
    Attempts to resolve a single enum type from a union of enum literals.

    If this cannot be resolved, the original is returned.
    """
    types = set()

    for item in typ.items:
        item = get_proper_type(item)
        if not isinstance(item, LiteralType) or not item.fallback.type.is_enum:
            # If anything that isn't a literal of an enum type is encountered, return the original.
            return typ
        types.add(item.fallback)

    # If there is only one enum type seen, return that otherwise return the original.
    return types.pop() if len(types) == 1 else typ


def transform_into_proper_attr_type(ctx: AttributeContext) -> MypyType:
    """
    A `get_attribute_hook` to make `.choices` and `.values` optional if `__empty__` is defined.

    When the `__empty__` label is specified, the `choices` and `values` properties can return a
    blank choice/value. This hook will amend the type returned by those properties.
    """
    if isinstance(ctx.context, MemberExpr):
        expr = ctx.context.expr
        name = ctx.context.name
    elif isinstance(ctx.context, SuperExpr):
        expr = ctx.context
        name = ctx.context.name
    else:
        ctx.api.fail("Unable to resolve type of property", ctx.context)
        return AnyType(TypeOfAny.from_error)

    node: TypeInfo | None = None

    if isinstance(expr, MemberExpr | NameExpr):
        if isinstance(expr.node, TypeInfo):
            node = expr.node
        elif isinstance(expr.node, TypeAlias):
            alias = get_proper_type(expr.node.target)
            if isinstance(alias, Instance):
                node = alias.type
    elif isinstance(expr, SuperExpr):
        node = expr.info

    _node_type: ProperType | None = None

    if node is None:
        _node_type = get_proper_type(ctx.api.get_expression_type(expr))
        if isinstance(_node_type, UnionType):
            # If this is a union of enum literals, check if they're all of the same enum type and
            # use that type instead. This situation often occurs where there is comparison to an
            # enum member in a branch.
            _node_type = get_proper_type(_get_enum_type_from_union_of_literals(_node_type))
        if isinstance(_node_type, LiteralType) and _node_type.is_enum_literal():
            _node_type = _node_type.fallback
        if isinstance(_node_type, TypeType):
            _node_type = _node_type.item
        if isinstance(_node_type, TypeVarType):
            _node_type = get_proper_type(_node_type.upper_bound)
        if isinstance(_node_type, Instance):
            node = _node_type.type
        if isinstance(_node_type, Overloaded) and _node_type.is_type_obj():
            node = _node_type.type_object()

    if node is None:
        if isinstance(_node_type, UnionType):
            # Suppress the error for a known case where there are multiple base choices types in a
            # union. In theory this is something that could be handled by extracting all of the
            # base types and making the following code consider all of these types, but that's
            # quite a bit of effort.
            return ctx.default_attr_type
        ctx.api.fail(f"Unable to resolve type of {name} property", ctx.context)
        return AnyType(TypeOfAny.from_error)

    default_attr_type = get_proper_type(ctx.default_attr_type)

    if not node.is_enum or not node.has_base(fullnames.CHOICES_CLASS_FULLNAME):
        return default_attr_type

    # Enums with more than one base will treat the first base as the mixed-in type.
    base_type = node.bases[0] if len(node.bases) > 1 else None

    # When `__empty__` is defined, the `.choices` and `.values` properties will include `None` for
    # the blank choice which is labelled by the value of `__empty__`.
    has_empty_label = node.get("__empty__") is not None

    # When `__empty__` is not a lazy string and the labels on all members are not lazy strings, the
    # label can be simplified to only be a simple string type. This keeps the benefits of accurate
    # typing when the lazy labels are being used, but reduces the pain of having to manage a union
    # of a simple and lazy string type where it's not necessary.
    has_lazy_label = _has_lazy_label(node)

    if (
        name == "choices"
        and isinstance(default_attr_type, Instance)
        and default_attr_type.type.fullname == "builtins.list"
        and len(default_attr_type.args) == 1
    ):
        choice_arg = get_proper_type(default_attr_type.args[0])

        if isinstance(choice_arg, TupleType) and choice_arg.length() == 2:
            value_arg, label_arg = choice_arg.items
            label_arg = get_proper_type(label_arg)
            value_arg = get_proper_type(value_arg)
            new_label_arg = _try_replace_label(label_arg, has_lazy_label)
            new_value_arg = _try_replace_value(value_arg, base_type, has_empty_label)
            if new_label_arg is not label_arg or new_value_arg is not value_arg:
                new_choice_arg = choice_arg.copy_modified(items=[new_value_arg, new_label_arg])
                return default_attr_type.copy_modified(args=[new_choice_arg])

    elif (
        name == "labels"
        and isinstance(default_attr_type, Instance)
        and default_attr_type.type.fullname == "builtins.list"
        and len(default_attr_type.args) == 1
    ):
        label_arg = get_proper_type(default_attr_type.args[0])
        new_label_arg = _try_replace_label(label_arg, has_lazy_label)
        if new_label_arg is not label_arg:
            return default_attr_type.copy_modified(args=[new_label_arg])

    elif (
        name == "values"
        and isinstance(default_attr_type, Instance)
        and default_attr_type.type.fullname == "builtins.list"
        and len(default_attr_type.args) == 1
    ):
        value_arg = get_proper_type(default_attr_type.args[0])
        new_value_arg = _try_replace_value(value_arg, base_type, has_empty_label)
        if new_value_arg is not value_arg:
            return default_attr_type.copy_modified(args=[new_value_arg])

    elif name in ("__empty__", "label"):
        return _try_replace_label(default_attr_type, has_lazy_label)

    elif name == "value":
        # Pass in `False` because `.value` will never return `None`.
        return _try_replace_value(default_attr_type, base_type, False)

    return default_attr_type
