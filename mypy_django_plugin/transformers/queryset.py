from collections import OrderedDict
from typing import List, Optional, cast

from mypy.checker import TypeChecker
from mypy.nodes import StrExpr, TypeInfo
from mypy.plugin import (
    AnalyzeTypeContext, CheckerPluginInterface, MethodContext,
)
from mypy.types import AnyType, Instance, Type, TypeOfAny

from mypy_django_plugin import helpers
from mypy_django_plugin.lookups import (
    LookupException, RelatedModelNode, resolve_lookup,
)


def get_queryset_model_arg(ret_type: Instance) -> Type:
    if ret_type.args:
        return ret_type.args[0]
    else:
        return AnyType(TypeOfAny.implementation_artifact)


def extract_proper_type_for_queryset_values(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    fields_arg_expr = ctx.args[ctx.callee_arg_names.index('fields')]
    if len(fields_arg_expr) == 0:
        # values_list/values with no args is not yet supported, so default to Any types for field types
        # It should in the future include all model fields, "extra" fields and "annotated" fields
        return ctx.default_return_type

    model_arg = get_queryset_model_arg(ctx.default_return_type)
    if isinstance(model_arg, Instance):
        model_type_info = model_arg.type
    else:
        model_type_info = None

    column_types: OrderedDict[str, Type] = OrderedDict()

    # parse *fields
    for field_expr in fields_arg_expr:
        if isinstance(field_expr, StrExpr):
            field_name = field_expr.value
            # Default to any type
            column_types[field_name] = AnyType(TypeOfAny.implementation_artifact)

            if model_type_info:
                resolved_lookup_type = resolve_values_lookup(ctx.api, model_type_info, field_name)
                if resolved_lookup_type is not None:
                    column_types[field_name] = resolved_lookup_type
        else:
            return ctx.default_return_type

    # parse **expressions
    expression_arg_names = ctx.arg_names[ctx.callee_arg_names.index('expressions')]
    for expression_name in expression_arg_names:
        # Arbitrary additional annotation expressions are supported, but they all have type Any for now
        column_types[expression_name] = AnyType(TypeOfAny.implementation_artifact)

    row_arg = helpers.make_typeddict(ctx.api, fields=column_types,
                                     required_keys=set())
    return helpers.reparametrize_instance(ctx.default_return_type, [model_arg, row_arg])


def extract_proper_type_queryset_values_list(ctx: MethodContext) -> Type:
    object_type = ctx.type
    if not isinstance(object_type, Instance):
        return ctx.default_return_type

    ret = ctx.default_return_type

    model_arg = get_queryset_model_arg(ctx.default_return_type)
    # model_arg: Union[AnyType, Type] = ret.args[0] if len(ret.args) > 0 else any_type

    column_names: List[Optional[str]] = []
    column_types: OrderedDict[str, Type] = OrderedDict()

    fields_arg_expr = ctx.args[ctx.callee_arg_names.index('fields')]
    fields_param_is_specified = True
    if len(fields_arg_expr) == 0:
        # values_list/values with no args is not yet supported, so default to Any types for field types
        # It should in the future include all model fields, "extra" fields and "annotated" fields
        fields_param_is_specified = False

    if isinstance(model_arg, Instance):
        model_type_info = model_arg.type
    else:
        model_type_info = None

    any_type = AnyType(TypeOfAny.implementation_artifact)

    # Figure out each field name passed to fields
    only_strings_as_fields_expressions = True
    for field_expr in fields_arg_expr:
        if isinstance(field_expr, StrExpr):
            field_name = field_expr.value
            column_names.append(field_name)
            # Default to any type
            column_types[field_name] = any_type

            if model_type_info:
                resolved_lookup_type = resolve_values_lookup(ctx.api, model_type_info, field_name)
                if resolved_lookup_type is not None:
                    column_types[field_name] = resolved_lookup_type
        else:
            # Dynamic field names are partially supported for values_list, but not values
            column_names.append(None)
            only_strings_as_fields_expressions = False

    flat = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'flat'))
    named = helpers.parse_bool(helpers.get_argument_by_name(ctx, 'named'))

    api = cast(TypeChecker, ctx.api)
    if named and flat:
        api.fail("'flat' and 'named' can't be used together.", ctx.context)
        return ret

    elif named:
        # named=True, flat=False -> List[NamedTuple]
        if fields_param_is_specified and only_strings_as_fields_expressions:
            row_arg = helpers.make_named_tuple(api, fields=column_types, name="Row")
        else:
            # fallback to catch-all NamedTuple
            row_arg = helpers.make_named_tuple(api, fields=OrderedDict(), name="Row")

    elif flat:
        # named=False, flat=True -> List of elements
        if len(ctx.args[0]) > 1:
            api.fail("'flat' is not valid when values_list is called with more than one field.",
                     ctx.context)
            return ctx.default_return_type

        if fields_param_is_specified and only_strings_as_fields_expressions:
            # Grab first element
            row_arg = column_types[column_names[0]]
        else:
            row_arg = any_type

    else:
        # named=False, flat=False -> List[Tuple]
        if fields_param_is_specified:
            args = [
                # Fallback to Any if the column name is unknown (e.g. dynamic)
                column_types.get(column_name, any_type) if column_name is not None else any_type
                for column_name in column_names
            ]
        else:
            args = [any_type]
        row_arg = helpers.make_tuple(api, fields=args)

    new_type_args = [model_arg, row_arg]
    return helpers.reparametrize_instance(ret, new_type_args)


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


def set_first_generic_param_as_default_for_second(fullname: str, ctx: AnalyzeTypeContext) -> Type:
    if not ctx.type.args:
        try:
            return ctx.api.named_type(fullname, [AnyType(TypeOfAny.explicit),
                                                 AnyType(TypeOfAny.explicit)])
        except KeyError:
            # really should never happen
            return AnyType(TypeOfAny.explicit)

    args = ctx.type.args
    if len(args) == 1:
        args = [args[0], args[0]]

    analyzed_args = [ctx.api.analyze_type(arg) for arg in args]
    try:
        return ctx.api.named_type(fullname, analyzed_args)
    except KeyError:
        # really should never happen
        return AnyType(TypeOfAny.explicit)
