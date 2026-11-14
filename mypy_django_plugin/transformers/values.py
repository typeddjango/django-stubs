"""`values()` and `values_list()` row types"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import FieldError
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy.maptype import map_instance_to_supertype
from mypy.subtypes import is_subtype
from mypy.types import AnyType, Instance, ProperType, TypedDictType, TypeOfAny, TypeVarType, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, LookupsAreUnsupported
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers.annotate import gather_expression_types

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.db.models.base import Model
    from mypy.nodes import Expression, TypeInfo
    from mypy.plugin import MethodContext


def get_field_type_from_lookup(
    ctx: MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    *,
    lookup: str,
    silent_on_error: bool = False,
) -> MypyType | None:
    try:
        lookup_field, model_cls = django_context.resolve_lookup_into_field(model_cls, lookup)
    except FieldError as exc:
        if not silent_on_error:
            ctx.api.fail(exc.args[0], ctx.context)
        return None
    except LookupsAreUnsupported:
        return AnyType(TypeOfAny.explicit)

    if lookup_field is None:
        return AnyType(TypeOfAny.implementation_artifact)
    if isinstance(lookup_field, RelatedField | ForeignObjectRel):
        model_cls = django_context.get_field_related_model_cls(lookup_field)
        lookup_field = django_context.get_primary_key_field(model_cls)

    api = helpers.get_typechecker_api(ctx)
    model_info = helpers.lookup_class_typeinfo(api, model_cls)
    return helpers.get_field_get_type(api, ctx.context, model_info, lookup_field.attname)


def get_values_list_row_type(
    ctx: MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    *,
    annotation_types: dict[str, MypyType],
    flat: bool,
    named: bool,
) -> MypyType:
    field_lookups = resolve_field_lookups(ctx.args[0], django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    typechecker_api = helpers.get_typechecker_api(ctx)
    model_info = helpers.lookup_class_typeinfo(typechecker_api, model_cls)
    if len(field_lookups) == 0:
        if flat:
            primary_key_field = django_context.get_primary_key_field(model_cls)
            lookup_type = get_field_type_from_lookup(ctx, django_context, model_cls, lookup=primary_key_field.attname)
            assert lookup_type is not None
            return lookup_type
        if named:
            column_types: dict[str, MypyType] = {}
            for field in django_context.get_model_fields(model_cls):
                column_type = helpers.get_field_get_type(typechecker_api, ctx.context, model_info, field.attname)
                column_types[field.attname] = column_type
            column_types.update(annotation_types)
            return helpers.make_oneoff_named_tuple(typechecker_api, "Row", column_types)
        # flat=False, named=False, all fields
        if annotation_types:
            return typechecker_api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.special_form)])
        field_lookups = []
        for field in django_context.get_model_fields(model_cls):
            field_lookups.append(field.attname)

    if len(field_lookups) > 1 and flat:
        typechecker_api.fail("'flat' is not valid when 'values_list' is called with more than one field", ctx.context)
        return AnyType(TypeOfAny.from_error)

    column_types = {}
    for field_lookup in field_lookups:
        if annotation_type := annotation_types.get(field_lookup):
            column_types[field_lookup] = annotation_type
            continue

        lookup_field_type = get_field_type_from_lookup(
            ctx,
            django_context,
            model_cls,
            lookup=field_lookup,
            silent_on_error=bool(annotation_types),
        )
        if lookup_field_type is None:
            if annotation_types:
                lookup_field_type = AnyType(TypeOfAny.from_omitted_generics)
            else:
                return AnyType(TypeOfAny.from_error)
        column_types[field_lookup] = lookup_field_type

    if flat:
        assert len(column_types) == 1
        row_type = next(iter(column_types.values()))
    elif named:
        row_type = helpers.make_oneoff_named_tuple(typechecker_api, "Row", column_types)
    else:
        # Since there may have been repeated field lookups, we cannot just use column_types.values here.
        # This is not the case in named above, because Django will error if duplicate fields are requested.
        resolved_column_types = [column_types[field_lookup] for field_lookup in field_lookups]
        row_type = helpers.make_tuple(typechecker_api, resolved_column_types)

    return row_type


def _mro_base(instance: Instance, fullname: str) -> TypeInfo | None:
    return next((base for base in instance.type.mro if base.fullname == fullname), None)


def _queryset_subclass_with_row(ctx: MethodContext, row: MypyType) -> Instance | None:
    """
    Rebuild the receiver's custom queryset with another row type, e.g. `MyQS[_M, _Row]` -> `MyQS[Book, Row]`.
    The stubs can't express it: https://github.com/python/typing/issues/548
    """
    qs: ProperType = ctx.type
    if isinstance(qs, Instance) and (manager_info := _mro_base(qs, fullnames.BASE_MANAGER_CLASS_FULLNAME)):
        qs = get_proper_type(map_instance_to_supertype(qs, manager_info).args[1])
    if not isinstance(qs, Instance) or not (queryset_info := _mro_base(qs, fullnames.QUERYSET_CLASS_FULLNAME)):
        return None

    # Which of the subclass's own type vars fills the `QuerySet` row slot?
    own_type_vars = qs.type.defn.type_vars
    model_var, row_var = map(
        get_proper_type, map_instance_to_supertype(Instance(qs.type, own_type_vars), queryset_info).args
    )
    if (
        not isinstance(row_var, TypeVarType)
        or row_var == model_var  # `QuerySet[_M]`: the row slot defaults to the model type var
        or not is_subtype(row, row_var.upper_bound)  # `QuerySet["Book"]`: the plugin bounds the row slot to `Book`
    ):
        return None
    return qs.copy_modified(
        args=[row if tv.id == row_var.id else arg for tv, arg in zip(own_type_vars, qs.args, strict=True)]
    )


def extract_proper_type_queryset_values_list(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return ctx.default_return_type

    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        return ctx.default_return_type

    flat = helpers.get_bool_call_argument_by_name(ctx, "flat", default=False)
    named = helpers.get_bool_call_argument_by_name(ctx, "named", default=False)

    if flat and named:
        ctx.api.fail("'flat' and 'named' can't be used together", ctx.context)
        return default_return_type.copy_modified(args=[django_model.typ, AnyType(TypeOfAny.from_error)])

    annotation_types = _get_annotation_field_types(django_model.typ) if django_model.is_annotated else {}
    row_type = get_values_list_row_type(
        ctx,
        django_context,
        django_model.cls,
        annotation_types=annotation_types,
        flat=flat,
        named=named,
    )
    ret = _queryset_subclass_with_row(ctx, row_type) or default_return_type.copy_modified(
        args=[django_model.typ, row_type]
    )
    if not named and (field_lookups := resolve_field_lookups(ctx.args[0], django_context)):
        # For non-named values_list, the row type does not encode column names.
        # Attach selected field names to the returned QuerySet instance so that
        # subsequent annotate() can make an informed decision about name conflicts.
        ret.extra_attrs = helpers.merge_extra_attrs(ret.extra_attrs, new_immutable=set(field_lookups))
    return ret


def resolve_field_lookups(lookup_exprs: Sequence[Expression], django_context: DjangoContext) -> list[str] | None:
    field_lookups = []
    for field_lookup_expr in lookup_exprs:
        field_lookup = helpers.resolve_string_attribute_value(field_lookup_expr, django_context)
        if field_lookup is None:
            return None
        field_lookups.append(field_lookup)
    return field_lookups


def _get_annotation_field_types(model_type: Instance) -> dict[str, MypyType]:
    """Extract annotation field types from an annotated model's TypedDict type argument."""
    if model_type.args:
        annotations = get_proper_type(model_type.args[0])
        if isinstance(annotations, TypedDictType):
            return dict(annotations.items)
    return {}


def extract_proper_type_queryset_values(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Extract proper return type for QuerySet.values(*fields, **expressions) method calls.

    See https://docs.djangoproject.com/en/stable/ref/models/querysets/#values
    """
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return ctx.default_return_type

    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        return ctx.default_return_type

    field_lookups = resolve_field_lookups(ctx.args[0], django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    annotation_types = _get_annotation_field_types(django_model.typ) if django_model.is_annotated else {}

    # Bare `.values()` case
    if len(field_lookups) == 0 and not ctx.args[1]:
        for field in django_context.get_model_fields(django_model.cls):
            field_lookups.append(field.attname)
        field_lookups.extend(annotation_types)
    column_types: dict[str, MypyType] = {}

    # Collect `*fields` types -- `.values("id", "name")`
    for field_lookup in field_lookups:
        # Check annotation fields first for annotated querysets
        if annotation_type := annotation_types.get(field_lookup):
            column_types[field_lookup] = annotation_type
            continue

        field_lookup_type = get_field_type_from_lookup(
            ctx,
            django_context,
            django_model.cls,
            lookup=field_lookup,
            silent_on_error=django_model.is_annotated,
        )
        if field_lookup_type is None:
            if django_model.is_annotated:
                column_types[field_lookup] = AnyType(TypeOfAny.from_omitted_generics)
            else:
                return default_return_type.copy_modified(args=[django_model.typ, AnyType(TypeOfAny.from_error)])
        else:
            column_types[field_lookup] = field_lookup_type

    # Collect `**expressions` types -- `.values(lower_name=Lower("name"), foo=F("name"))`
    column_types.update(gather_expression_types(ctx))
    row_type = helpers.make_typeddict(ctx.api, column_types)
    return _queryset_subclass_with_row(ctx, row_type) or default_return_type.copy_modified(
        args=[django_model.typ, row_type]
    )
