from typing import cast

from mypy.checker import TypeChecker
from mypy.nodes import ListExpr, NameExpr, TupleExpr
from mypy.plugin import FunctionContext
from mypy.types import Instance, TupleType, Type

from mypy_django_plugin import helpers
from mypy_django_plugin.plugins.models import iter_over_assignments


def determine_type_of_array_field(ctx: FunctionContext) -> Type:
    base_field_arg_type = helpers.get_argument_type_by_name(ctx, 'base_field')
    if not base_field_arg_type or not isinstance(base_field_arg_type, Instance):
        return ctx.default_return_type

    get_method = base_field_arg_type.type.get_method('__get__')
    if not get_method:
        # not a method
        return ctx.default_return_type

    return ctx.api.named_generic_type(ctx.context.callee.fullname,
                                      args=[get_method.type.ret_type])


def record_field_properties_into_outer_model_class(ctx: FunctionContext) -> Type:
    api = cast(TypeChecker, ctx.api)
    outer_model = api.scope.active_class()
    if outer_model is None or not outer_model.has_base(helpers.MODEL_CLASS_FULLNAME):
        # outside models.Model class, undetermined
        return ctx.default_return_type

    field_name = None
    for name_expr, stmt in iter_over_assignments(outer_model.defn):
        if stmt == ctx.context and isinstance(name_expr, NameExpr):
            field_name = name_expr.name
            break
    if field_name is None:
        return ctx.default_return_type

    fields_metadata = outer_model.metadata.setdefault('django', {}).setdefault('fields', {})

    # primary key
    is_primary_key = False
    primary_key_arg = helpers.get_argument_by_name(ctx, 'primary_key')
    if primary_key_arg:
        is_primary_key = helpers.parse_bool(primary_key_arg)
    fields_metadata[field_name] = {'primary_key': is_primary_key}

    # choices
    choices_arg = helpers.get_argument_by_name(ctx, 'choices')
    if choices_arg and isinstance(choices_arg, (TupleExpr, ListExpr)):
        # iterable of 2 element tuples of two kinds
        _, analyzed_choices = api.analyze_iterable_item_type(choices_arg)
        if isinstance(analyzed_choices, TupleType):
            first_element_type = analyzed_choices.items[0]
            if isinstance(first_element_type, Instance):
                fields_metadata[field_name]['choices'] = first_element_type.type.fullname()

    # nullability
    null_arg = helpers.get_argument_by_name(ctx, 'null')
    is_nullable = False
    if null_arg:
        is_nullable = helpers.parse_bool(null_arg)
    fields_metadata[field_name]['null'] = is_nullable

    # is_blankable
    blank_arg = helpers.get_argument_by_name(ctx, 'blank')
    is_blankable = False
    if blank_arg:
        is_blankable = helpers.parse_bool(blank_arg)
    fields_metadata[field_name]['blank'] = is_blankable

    return ctx.default_return_type
