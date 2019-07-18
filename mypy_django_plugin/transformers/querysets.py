from collections import OrderedDict
from typing import Optional, Tuple, Type, Sequence, List, Union

from django.core.exceptions import FieldError
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from mypy.nodes import NameExpr, Expression
from mypy.plugin import AnalyzeTypeContext, FunctionContext, MethodContext
from mypy.types import AnyType, Instance, Type as MypyType, TypeOfAny

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import fullnames, helpers


def set_first_generic_param_as_default_for_second(ctx: AnalyzeTypeContext, fullname: str) -> MypyType:
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
    ctx.api.analyze_type(ctx.type)
    try:
        return ctx.api.named_type(fullname, analyzed_args)
    except KeyError:
        return AnyType(TypeOfAny.explicit)


def determine_proper_manager_type(ctx: FunctionContext) -> MypyType:
    ret = ctx.default_return_type
    assert isinstance(ret, Instance)

    if not ctx.api.tscope.classes:
        # not in class
        return ret
    outer_model_info = ctx.api.tscope.classes[0]
    if not outer_model_info.has_base(fullnames.MODEL_CLASS_FULLNAME):
        return ret

    return helpers.reparametrize_instance(ret, [Instance(outer_model_info, [])])


def get_lookup_field_get_type(ctx: MethodContext, django_context: DjangoContext, model_cls: Type[Model],
                              lookup: str, method: str) -> Optional[Tuple[str, MypyType]]:
    try:
        lookup_field = django_context.lookups_context.resolve_lookup(model_cls, lookup)
    except FieldError as exc:
        ctx.api.fail(exc.args[0], ctx.context)
        return None

    field_get_type = django_context.fields_context.get_field_get_type(ctx.api, lookup_field, method)
    return lookup, field_get_type


def get_values_list_row_type(ctx: MethodContext, django_context: DjangoContext, model_cls: Type[Model],
                             flat: bool, named: bool) -> MypyType:
    field_lookups = resolve_field_lookups(ctx.args[0], ctx, django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    if len(field_lookups) == 0:
        if flat:
            primary_key_field = django_context.get_primary_key_field(model_cls)
            _, column_type = get_lookup_field_get_type(ctx, django_context, model_cls,
                                                          primary_key_field.attname, 'values_list')
            return column_type
        elif named:
            column_types = OrderedDict()
            for field in django_context.get_model_fields(model_cls):
                column_type = django_context.fields_context.get_field_get_type(ctx.api, field, 'values_list')
                column_types[field.attname] = column_type
            return helpers.make_oneoff_named_tuple(ctx.api, 'Row', column_types)
        else:
            # flat=False, named=False, all fields
            field_lookups = []
            for field in django_context.get_model_fields(model_cls):
                field_lookups.append(field.attname)

    if len(field_lookups) > 1 and flat:
        ctx.api.fail("'flat' is not valid when 'values_list' is called with more than one field", ctx.context)
        return AnyType(TypeOfAny.from_error)

    column_types = OrderedDict()
    for field_lookup in field_lookups:
        result = get_lookup_field_get_type(ctx, django_context, model_cls, field_lookup, 'values_list')
        if result is None:
            return AnyType(TypeOfAny.from_error)

        column_name, column_type = result
        column_types[column_name] = column_type

    if flat:
        assert len(column_types) == 1
        row_type = next(iter(column_types.values()))
    elif named:
        row_type = helpers.make_oneoff_named_tuple(ctx.api, 'Row', column_types)
    else:
        row_type = helpers.make_tuple(ctx.api, list(column_types.values()))

    return row_type


def extract_proper_type_queryset_values_list(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    # called on the Instance
    assert isinstance(ctx.type, Instance)

    # bail if queryset of Any or other non-instances
    if not isinstance(ctx.type.args[0], Instance):
        return AnyType(TypeOfAny.from_omitted_generics)

    model_type = ctx.type.args[0]
    model_cls = django_context.get_model_class_by_fullname(model_type.type.fullname())
    if model_cls is None:
        return ctx.default_return_type

    flat_expr = helpers.get_call_argument_by_name(ctx, 'flat')
    if flat_expr is not None and isinstance(flat_expr, NameExpr):
        flat = helpers.parse_bool(flat_expr)
    else:
        flat = False

    named_expr = helpers.get_call_argument_by_name(ctx, 'named')
    if named_expr is not None and isinstance(named_expr, NameExpr):
        named = helpers.parse_bool(named_expr)
    else:
        named = False

    if flat and named:
        ctx.api.fail("'flat' and 'named' can't be used together", ctx.context)
        return helpers.reparametrize_instance(ctx.default_return_type, [model_type, AnyType(TypeOfAny.from_error)])

    row_type = get_values_list_row_type(ctx, django_context, model_cls,
                                        flat=flat, named=named)
    return helpers.reparametrize_instance(ctx.default_return_type, [model_type, row_type])


def resolve_field_lookups(lookup_exprs: Sequence[Expression], ctx: Union[FunctionContext, MethodContext],
                          django_context: DjangoContext) -> Optional[List[str]]:
    field_lookups = []
    for field_lookup_expr in lookup_exprs:
        field_lookup = helpers.resolve_string_attribute_value(field_lookup_expr, ctx, django_context)
        if field_lookup is None:
            return None
        field_lookups.append(field_lookup)
    return field_lookups


def extract_proper_type_queryset_values(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    # queryset method
    assert isinstance(ctx.type, Instance)
    # if queryset of non-instance type
    if not isinstance(ctx.type.args[0], Instance):
        return AnyType(TypeOfAny.from_omitted_generics)

    model_type = ctx.type.args[0]
    model_cls = django_context.get_model_class_by_fullname(model_type.type.fullname())
    if model_cls is None:
        return ctx.default_return_type

    field_lookups = resolve_field_lookups(ctx.args[0], ctx, django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    if len(field_lookups) == 0:
        for field in django_context.get_model_fields(model_cls):
            field_lookups.append(field.attname)

    column_types = OrderedDict()
    for field_lookup in field_lookups:
        result = get_lookup_field_get_type(ctx, django_context, model_cls, field_lookup, 'values')
        if result is None:
            return helpers.reparametrize_instance(ctx.default_return_type, [model_type, AnyType(TypeOfAny.from_error)])

        column_name, column_type = result
        column_types[column_name] = column_type

    row_type = helpers.make_typeddict(ctx.api, column_types, set(column_types.keys()))
    return helpers.reparametrize_instance(ctx.default_return_type, [model_type, row_type])
