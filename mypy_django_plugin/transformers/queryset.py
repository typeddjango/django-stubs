from collections import OrderedDict
from typing import Union, Dict, List, cast, Optional

from mypy.checker import TypeChecker
from mypy.nodes import StrExpr, TypeInfo
from mypy.plugin import MethodContext, CheckerPluginInterface
from mypy.types import Type, Instance, AnyType, TypeOfAny

from mypy_django_plugin import helpers
from mypy_django_plugin.lookups import resolve_lookup, RelatedModelNode, LookupException


def extract_proper_type_for_values_and_values_list(method_name: str, ctx: MethodContext) -> Type:
    api = cast(TypeChecker, ctx.api)

    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    ret = ctx.default_return_type

    any_type = AnyType(TypeOfAny.implementation_artifact)
    fields_arg_expr = ctx.args[ctx.callee_arg_names.index('fields')]

    model_arg: Union[AnyType, Type] = ret.args[0] if len(ret.args) > 0 else any_type

    field_names: List[str] = []
    field_types: OrderedDict[str, Type] = OrderedDict()

    fill_field_types = True

    if len(fields_arg_expr) == 0:
        # values_list/values with no args is not yet supported, so default to Any types for field types
        # It should in the future include all model fields, "extra" fields and "annotated" fields
        fill_field_types = False

    # Figure out each field name passed to fields
    for field_expr in fields_arg_expr:
        if not isinstance(field_expr, StrExpr):
            # Dynamic field names are not supported (partial support is possible for values_list, but not values)
            fill_field_types = False
            break
        field_name = field_expr.value
        field_names.append(field_name)

        # Default to any type
        field_types[field_name] = any_type

    if fill_field_types:
        if isinstance(model_arg, Instance):
            model_type_info = model_arg.type
            field_types = refine_values_lookup_types(ctx, field_types, model_type_info)

    if method_name == 'values_list':
        flat = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'flat'))
        named = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'named'))

        if named and flat:
            api.fail("'flat' and 'named' can't be used together.", ctx.context)
            return ret
        elif named:
            if fill_field_types:
                row_arg = helpers.make_named_tuple(api, fields=field_types, name="Row")
            else:
                row_arg = helpers.make_named_tuple(api, fields=OrderedDict(), name="Row")
        elif flat:
            if len(ctx.args[0]) > 1:
                api.fail("'flat' is not valid when values_list is called with more than one field.", ctx.context)
                return ret
            if fill_field_types:
                row_arg = field_types[field_names[0]]
            else:
                row_arg = any_type
        else:
            if fill_field_types:
                args = [
                    field_types[field_name]
                    for field_name in field_names
                ]
            else:
                args = [any_type]
            row_arg = helpers.make_tuple(api, fields=args)
    elif method_name == 'values':
        if fill_field_types:
            row_arg = helpers.make_typeddict(api, fields=field_types, required_keys=set())
        else:
            return ctx.default_return_type
    else:
        raise Exception(f"extract_proper_type_for_values_list doesn't support method {method_name}")

    new_type_args = [model_arg, row_arg]
    return helpers.reparametrize_instance(ret, new_type_args)


def refine_values_lookup_types(ctx, lookup_types: Dict[str, Type], model_type_info: TypeInfo) -> Dict[str, Type]:
    new_lookup_types = {}
    for lookup in lookup_types.keys():
        resolved_lookup_type = resolve_values_lookup(ctx.api, model_type_info, lookup)
        # Try to resolve the lookup type. If not able to resolve, fallback to the original type
        new_lookup_types[lookup] = resolved_lookup_type if resolved_lookup_type is not None else lookup_types[lookup]
    return new_lookup_types


def resolve_values_lookup(api: CheckerPluginInterface, model_type_info: TypeInfo, lookup: str) -> Optional[Type]:
    """Resolves a values/values_list lookup if possible, to a Type."""
    try:
        nodes = resolve_lookup(api, model_type_info, lookup)
    except LookupException:
        nodes = []

    if not nodes:
        return None

    make_optional = False

    for node in nodes:
        if isinstance(node, RelatedModelNode) and node.is_nullable:
            # All lookups following a relation which is nullable should be optional
            make_optional = True

    node = nodes[-1]

    node_type = node.typ
    if isinstance(node, RelatedModelNode):
        # Related models used in values/values_list get resolved to the primary key of the related model.
        # So, we lookup the pk of that model.
        pk_lookup_nodes = resolve_lookup(api, node_type.type, "pk")
        if not pk_lookup_nodes:
            return None
        node_type = pk_lookup_nodes[0].typ
    if make_optional:
        return helpers.make_optional(node_type)
    else:
        return node_type
