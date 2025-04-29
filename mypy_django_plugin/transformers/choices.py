from mypy.nodes import MemberExpr, NameExpr, TypeAlias, TypeInfo
from mypy.plugin import AttributeContext
from mypy.typeanal import make_optional_type
from mypy.types import (
    AnyType,
    Instance,
    LiteralType,
    TupleType,
    TypeOfAny,
    TypeType,
    TypeVarType,
    UnionType,
    get_proper_type,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import fullnames, helpers


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

    if node is None:
        _node_type = get_proper_type(ctx.api.get_expression_type(expr))
        if isinstance(_node_type, UnionType):
            # If this is a union of enum literals, check if they're all of the same enum type and
            # use that type instead. This situation often occurs where there is comparison to an
            # enum member in a branch.
            _node_type = get_proper_type(_get_enum_type_from_union_of_literals(_node_type))
        if isinstance(_node_type, TypeType):
            _node_type = _node_type.item
        if isinstance(_node_type, TypeVarType):
            _node_type = get_proper_type(_node_type.upper_bound)
        if isinstance(_node_type, Instance):
            node = _node_type.type

    if node is None:
        ctx.api.fail(f"Unable to resolve type of {name} property", ctx.context)
        return AnyType(TypeOfAny.from_error)

    default_attr_type = get_proper_type(ctx.default_attr_type)

    if not node.is_enum or not node.has_base(fullnames.CHOICES_CLASS_FULLNAME):
        return default_attr_type

    # Enums with more than one base will treat the first base as the mixed-in type.
    base_type = node.bases[0] if len(node.bases) > 1 else None

    # When `__empty__` is defined, the `.choices` and `.values` properties will include `None` for
    # the blank choice which is labelled by the value of `__empty__`.
    has_blank_choice = node.get("__empty__") is not None

    if (
        name == "choices"
        and isinstance(default_attr_type, Instance)
        and default_attr_type.type.fullname == "builtins.list"
        and len(default_attr_type.args) == 1
    ):
        choice_arg = get_proper_type(default_attr_type.args[0])

        if isinstance(choice_arg, TupleType) and choice_arg.length() == 2:
            value_arg, label_arg = choice_arg.items
            value_arg = get_proper_type(value_arg)

            if isinstance(value_arg, AnyType) and base_type is not None:
                new_value_arg = make_optional_type(base_type) if has_blank_choice else base_type
                new_choice_arg = choice_arg.copy_modified(items=[new_value_arg, label_arg])
                return helpers.reparametrize_instance(default_attr_type, [new_choice_arg])

            elif has_blank_choice:
                new_value_arg = make_optional_type(value_arg)
                new_choice_arg = choice_arg.copy_modified(items=[new_value_arg, label_arg])
                return helpers.reparametrize_instance(default_attr_type, [new_choice_arg])

    elif (
        name == "values"
        and isinstance(default_attr_type, Instance)
        and default_attr_type.type.fullname == "builtins.list"
        and len(default_attr_type.args) == 1
    ):
        value_arg = get_proper_type(default_attr_type.args[0])

        if isinstance(value_arg, AnyType) and base_type is not None:
            new_value_arg = make_optional_type(base_type) if has_blank_choice else base_type
            return helpers.reparametrize_instance(default_attr_type, [new_value_arg])

        elif has_blank_choice:
            new_value_arg = make_optional_type(value_arg)
            return helpers.reparametrize_instance(default_attr_type, [new_value_arg])

    elif name == "value" and isinstance(default_attr_type, AnyType) and base_type is not None:
        return base_type

    return default_attr_type
