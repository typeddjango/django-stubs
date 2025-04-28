from mypy.nodes import MemberExpr, NameExpr, TypeInfo, Var
from mypy.plugin import AttributeContext
from mypy.typeanal import make_optional_type
from mypy.types import AnyType, Instance, TupleType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import fullnames, helpers


def transform_into_proper_attr_type(ctx: AttributeContext) -> MypyType:
    """
    A `get_attribute_hook` to make `.choices` and `.values` optional if `__empty__` is defined.

    When the `__empty__` label is specified, the `choices` and `values` properties can return a
    blank choice/value. This hook will amend the type returned by those properties.
    """
    if isinstance(ctx.context, MemberExpr):
        method_name = ctx.context.name
    else:
        ctx.api.fail("Unable to resolve type of choices property", ctx.context)
        return AnyType(TypeOfAny.from_error)

    expr = ctx.context.expr

    if isinstance(expr, MemberExpr):
        expr = expr.expr

    if isinstance(expr, NameExpr) and isinstance(expr.node, TypeInfo):
        node = expr.node
    elif (
        isinstance(expr, NameExpr)
        and isinstance(expr.node, Var)
        and isinstance(var_node_type := get_proper_type(expr.node.type), Instance)
    ):
        node = var_node_type.type
    else:
        ctx.api.fail("Unable to resolve type of choices property", ctx.context)
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
        method_name == "choices"
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
        method_name == "values"
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

    elif method_name == "value" and isinstance(default_attr_type, AnyType) and base_type is not None:
        return base_type

    return default_attr_type
