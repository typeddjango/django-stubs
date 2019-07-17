from collections import OrderedDict
from typing import Optional, Tuple, Type

from django.core.exceptions import FieldError
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from mypy.nodes import NameExpr
from mypy.plugin import AnalyzeTypeContext, FunctionContext, MethodContext
from mypy.types import AnyType, Instance, Type as MypyType, TypeOfAny

from mypy_django_plugin_newsemanal.django.context import DjangoContext
from mypy_django_plugin_newsemanal.lib import fullnames, helpers


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
    return lookup_field.attname, field_get_type


def get_values_list_row_type(ctx: MethodContext, django_context: DjangoContext, model_cls: Type[Model],
                             flat: bool, named: bool) -> MypyType:
    field_lookups = [expr.value for expr in ctx.args[0]]
    if len(field_lookups) == 0:
        if flat:
            primary_key_field = django_context.get_primary_key_field(model_cls)
            _, field_get_type = get_lookup_field_get_type(ctx, django_context, model_cls,
                                                          primary_key_field.attname, 'values_list')
            return field_get_type
        elif named:
            column_types = OrderedDict()
            for field in django_context.get_model_fields(model_cls):
                field_get_type = django_context.fields_context.get_field_get_type(ctx.api, field, 'values_list')
                column_types[field.attname] = field_get_type
            return helpers.make_oneoff_named_tuple(ctx.api, 'Row', column_types)
        else:
            # flat=False, named=False, all fields
            field_lookups = []
            for field in model_cls._meta.get_fields():
                field_lookups.append(field.attname)

    if len(field_lookups) > 1 and flat:
        ctx.api.fail("'flat' is not valid when 'values_list' is called with more than one field", ctx.context)
        return AnyType(TypeOfAny.from_error)

    column_types = OrderedDict()
    for field_lookup in field_lookups:
        result = get_lookup_field_get_type(ctx, django_context, model_cls, field_lookup, 'values_list')
        if result is None:
            return AnyType(TypeOfAny.from_error)
        field_name, field_get_type = result
        column_types[field_name] = field_get_type

    if flat:
        assert len(column_types) == 1
        row_type = next(iter(column_types.values()))
    elif named:
        row_type = helpers.make_oneoff_named_tuple(ctx.api, 'Row', column_types)
    else:
        row_type = helpers.make_tuple(ctx.api, list(column_types.values()))

    return row_type


def extract_proper_type_queryset_values_list(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    assert isinstance(ctx.type, Instance)
    assert isinstance(ctx.type.args[0], Instance)

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


def extract_proper_type_queryset_values(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    assert isinstance(ctx.type, Instance)
    assert isinstance(ctx.type.args[0], Instance)

    model_type = ctx.type.args[0]
    model_cls = django_context.get_model_class_by_fullname(model_type.type.fullname())
    if model_cls is None:
        return ctx.default_return_type

    field_lookups = [expr.value for expr in ctx.args[0]]
    if len(field_lookups) == 0:
        for field in model_cls._meta.get_fields():
            field_lookups.append(field.attname)

    column_types = OrderedDict()
    for field_lookup in field_lookups:
        try:
            lookup_field = django_context.lookups_context.resolve_lookup(model_cls, field_lookup)
        except FieldError as exc:
            ctx.api.fail(exc.args[0], ctx.context)
            return helpers.reparametrize_instance(ctx.default_return_type, [model_type, AnyType(TypeOfAny.from_error)])

        field_get_type = django_context.fields_context.get_field_get_type(ctx.api, lookup_field, 'values')
        field_name = lookup_field.attname
        if isinstance(lookup_field, ForeignKey) and field_lookup == lookup_field.name:
            field_name = lookup_field.name

        column_types[field_name] = field_get_type

    row_type = helpers.make_typeddict(ctx.api, column_types, set(column_types.keys()))
    return helpers.reparametrize_instance(ctx.default_return_type, [model_type, row_type])
