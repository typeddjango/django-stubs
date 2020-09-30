import collections
from typing import List, Optional, Sequence, Type

from django.core.exceptions import FieldError
from django.db.models.base import Model
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy.nodes import Expression, NameExpr
from mypy.plugin import MethodContext
from mypy.types import AnyType, Instance
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny

from mypy_django_plugin.django.context import (
    DjangoContext, LookupsAreUnsupported,
)
from mypy_django_plugin.lib import chk_helpers, fullnames, helpers


def get_field_type_from_lookup(ctx: MethodContext, django_context: DjangoContext, model_cls: Type[Model],
                               *, method: str, lookup: str) -> Optional[MypyType]:
    try:
        lookup_field = django_context.resolve_lookup_into_field(model_cls, lookup)
    except FieldError as exc:
        ctx.api.fail(exc.args[0], ctx.context)
        return None
    except LookupsAreUnsupported:
        return AnyType(TypeOfAny.explicit)

    if ((isinstance(lookup_field, RelatedField) and lookup_field.column == lookup)
            or isinstance(lookup_field, ForeignObjectRel)):
        related_model_cls = django_context.get_field_related_model_cls(lookup_field)
        if related_model_cls is None:
            return AnyType(TypeOfAny.from_error)
        lookup_field = django_context.get_primary_key_field(related_model_cls)

    field_get_type = django_context.get_field_get_type(chk_helpers.get_typechecker_api(ctx),
                                                       lookup_field, method=method)
    return field_get_type


def resolve_field_lookups(lookup_exprs: Sequence[Expression], django_context: DjangoContext) -> Optional[List[str]]:
    field_lookups = []
    for field_lookup_expr in lookup_exprs:
        field_lookup = helpers.resolve_string_attribute_value(field_lookup_expr, django_context)
        if field_lookup is None:
            return None
        field_lookups.append(field_lookup)
    return field_lookups


def get_values_list_row_type(ctx: MethodContext, django_context: DjangoContext, model_cls: Type[Model],
                             flat: bool, named: bool) -> MypyType:
    field_lookups = resolve_field_lookups(ctx.args[0], django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    typechecker_api = chk_helpers.get_typechecker_api(ctx)
    if len(field_lookups) == 0:
        if flat:
            primary_key_field = django_context.get_primary_key_field(model_cls)
            lookup_type = get_field_type_from_lookup(ctx, django_context, model_cls,
                                                     lookup=primary_key_field.attname, method='values_list')
            assert lookup_type is not None
            return lookup_type
        elif named:
            column_types = collections.OrderedDict()
            for field in django_context.get_model_fields(model_cls):
                column_type = django_context.get_field_get_type(typechecker_api, field,
                                                                method='values_list')
                column_types[field.attname] = column_type
            return chk_helpers.make_oneoff_named_tuple(typechecker_api, 'Row', column_types)
        else:
            # flat=False, named=False, all fields
            field_lookups = []
            for field in django_context.get_model_fields(model_cls):
                field_lookups.append(field.attname)

    if len(field_lookups) > 1 and flat:
        typechecker_api.fail("'flat' is not valid when 'values_list' is called with more than one field", ctx.context)
        return AnyType(TypeOfAny.from_error)

    column_types = collections.OrderedDict()
    for field_lookup in field_lookups:
        lookup_field_type = get_field_type_from_lookup(ctx, django_context, model_cls,
                                                       lookup=field_lookup, method='values_list')
        if lookup_field_type is None:
            return AnyType(TypeOfAny.from_error)
        column_types[field_lookup] = lookup_field_type

    if flat:
        assert len(column_types) == 1
        row_type = next(iter(column_types.values()))
    elif named:
        row_type = chk_helpers.make_oneoff_named_tuple(typechecker_api, 'Row', column_types)
    else:
        row_type = chk_helpers.make_tuple(typechecker_api, list(column_types.values()))

    return row_type


class QuerySetMethodCallback(helpers.GetMethodCallback):
    def current_model_type(self) -> Optional[Instance]:
        for base_type in [self.callee_type, *self.callee_type.type.bases]:
            if (len(base_type.args)
                    and isinstance(base_type.args[0], Instance)
                    and base_type.args[0].type.has_base(fullnames.MODEL_CLASS_FULLNAME)):
                return base_type.args[0]
        return None


class QuerySetValuesCallback(QuerySetMethodCallback):
    def get_method_return_type(self) -> MypyType:
        assert isinstance(self.default_return_type, Instance)

        model_type = self.current_model_type()
        if model_type is None:
            return AnyType(TypeOfAny.from_omitted_generics)

        model_cls = self.django_context.get_model_class_by_fullname(model_type.type.fullname)
        if model_cls is None:
            return self.default_return_type

        field_lookups = resolve_field_lookups(self.ctx.args[0], self.django_context)
        if field_lookups is None:
            return AnyType(TypeOfAny.from_error)

        if len(field_lookups) == 0:
            for field in self.django_context.get_model_fields(model_cls):
                field_lookups.append(field.attname)

        column_types = collections.OrderedDict()
        for field_lookup in field_lookups:
            field_lookup_type = get_field_type_from_lookup(self.ctx, self.django_context, model_cls,
                                                           lookup=field_lookup, method='values')
            if field_lookup_type is None:
                return helpers.reparametrize_instance(self.default_return_type,
                                                      [model_type, AnyType(TypeOfAny.from_error)])

            column_types[field_lookup] = field_lookup_type

        row_type = chk_helpers.make_oneoff_typeddict(self.ctx.api, column_types, set(column_types.keys()))
        return helpers.reparametrize_instance(self.default_return_type, [model_type, row_type])


class QuerySetValuesListCallback(QuerySetMethodCallback):
    def get_method_return_type(self) -> MypyType:
        # called on the Instance, returns QuerySet of something
        assert isinstance(self.default_return_type, Instance)

        model_type = self.current_model_type()
        if model_type is None:
            return AnyType(TypeOfAny.from_omitted_generics)

        model_cls = self.django_context.get_model_class_by_fullname(model_type.type.fullname)
        if model_cls is None:
            return self.default_return_type

        flat_expr = chk_helpers.get_call_argument_by_name(self.ctx, 'flat')
        if flat_expr is not None and isinstance(flat_expr, NameExpr):
            flat = helpers.parse_bool(flat_expr)
        else:
            flat = False

        named_expr = chk_helpers.get_call_argument_by_name(self.ctx, 'named')
        if named_expr is not None and isinstance(named_expr, NameExpr):
            named = helpers.parse_bool(named_expr)
        else:
            named = False

        if flat and named:
            self.ctx.api.fail("'flat' and 'named' can't be used together", self.ctx.context)
            return helpers.reparametrize_instance(self.default_return_type, [model_type, AnyType(TypeOfAny.from_error)])

        # account for possible None
        flat = flat or False
        named = named or False

        row_type = get_values_list_row_type(self.ctx, self.django_context, model_cls,
                                            flat=flat, named=named)
        return helpers.reparametrize_instance(self.default_return_type, [model_type, row_type])
