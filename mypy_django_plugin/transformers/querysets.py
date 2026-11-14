"""Field name validation

Field names passed as strings are resolved like Django does at runtime, async variants included:

| Method | Accepts |
| --- | --- |
| `select_related()` | foreign key and one-to-one relations |
| `order_by()`, `earliest()`, `latest()` | fields, relations, transforms like `__year` and annotations |
| `distinct()` | like `order_by()`, without the `-` prefix |
| `defer()`, `only()` | fields and relations |
| `update()` | concrete fields |
| `in_bulk(field_name=...)` | unique fields, or the field the queryset is `distinct()` on |
| `bulk_update(fields=...)`, `bulk_create(update_fields=...)` | concrete fields other than the primary key |
| `bulk_create(unique_fields=...)` | concrete fields |

```python
Book.objects.latest("nope")  # error: Cannot resolve keyword 'nope' into field. Choices are: ...  [misc]
Book.objects.update(tags=1)  # error: "update()" can only be used with concrete fields. Got "tags"  [misc]
```
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal

from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.query import Query
from mypy.errorcodes import NO_REDEF
from mypy.nodes import ARG_NAMED, ARG_NAMED_OPT, ListExpr, SetExpr, TupleExpr
from mypy.types import AnyType, Instance, TupleType, TypedDictType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, LookupsAreUnsupported
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.lib.field_validation import (
    check_field_concrete,
    check_field_unique,
    try_get_field,
    validate_non_pk_concrete_field,
)

if TYPE_CHECKING:
    from django.db.models.base import Model
    from mypy.plugin import MethodContext

    from mypy_django_plugin.lib.helpers import DjangoModel


def _get_selected_fields_from_queryset_type(qs_type: Instance) -> set[str] | None:
    """
    Derive selected field names from a QuerySet type.

    Sources:
      - values(): encoded in the row TypedDict keys
      - values_list(named=True): row is a NamedTuple; extract field names from fallback TypeInfo
      - values_list(named=False): stored in qs_type.extra_attrs.immutable
    """
    if qs_type.type.has_base(fullnames.BASE_MANAGER_CLASS_FULLNAME):
        # A manager yields full model rows, its second type arg is the queryset, not a row type.
        return None
    if len(qs_type.args) > 1:
        row_type = get_proper_type(qs_type.args[1])
        if isinstance(row_type, Instance) and helpers.is_model_type(row_type.type):
            return None
        if isinstance(row_type, TypedDictType):
            return set(row_type.items.keys())
        if isinstance(row_type, TupleType):
            if row_type.partial_fallback.type.has_base("typing.NamedTuple"):
                return {name for name, sym in row_type.partial_fallback.type.names.items() if sym.plugin_generated}
            return set()
        return set()

    # Fallback to explicit metadata attached to the QuerySet Instance
    if qs_type.extra_attrs and qs_type.extra_attrs.immutable and isinstance(qs_type.extra_attrs.immutable, set):
        return qs_type.extra_attrs.immutable

    return None


_DISTINCT_FIELD_ATTR_PREFIX: Final = "__distinct_field__:"
_DISTINCT_FIELD_UNKNOWN_ATTR: Final = f"{_DISTINCT_FIELD_ATTR_PREFIX}*"


def _is_distinct_on_field(qs_type: Instance, field_name: str) -> bool:
    # mirrors Django's in_bulk() carve-out: self.query.distinct_fields != (field_name,)
    if not qs_type.extra_attrs:
        return False
    attrs = qs_type.extra_attrs.attrs
    return _DISTINCT_FIELD_UNKNOWN_ATTR in attrs or f"{_DISTINCT_FIELD_ATTR_PREFIX}{field_name}" in attrs


def _get_annotated_fields_from_queryset_type(qs_type: Instance) -> set[str]:
    """
    Derive annotated field names from a QuerySet type.

    Sources:
      - args[0].extra_attrs: from .annotate() calls
      - args[1].extra_attrs: from WithAnnotations[Model, TypedDict]
    """
    fields: set[str] = set()

    if len(qs_type.args) >= 1:
        model_type = get_proper_type(qs_type.args[0])
        if isinstance(model_type, Instance) and model_type.extra_attrs:
            fields.update(model_type.extra_attrs.attrs.keys())

    if len(qs_type.args) >= 2:
        row_type = get_proper_type(qs_type.args[1])
        if isinstance(row_type, Instance) and row_type.extra_attrs:
            fields.update(row_type.extra_attrs.attrs.keys())

    return fields


def check_valid_attr_value(
    ctx: MethodContext,
    django_context: DjangoContext,
    model: DjangoModel,
    attr_name: str,
    *,
    new_attr_names: set[str] | None = None,
) -> bool:
    """
    Check if adding `attr_name` would conflict with existing symbols on `model`.

    Args:
        - model: The Django model being analyzed
        - attr_name: The name of the attribute to be added
        - new_attr_names: A mapping of field names to types currently being added to the model
    """
    deselected_fields: set[str] | None = None
    annotated_fields: set[str] = set()
    if isinstance(ctx.type, Instance):
        selected_fields = _get_selected_fields_from_queryset_type(ctx.type)
        if selected_fields is not None:
            model_field_names = {f.name for f in django_context.get_model_fields(model.cls)}
            deselected_fields = model_field_names - selected_fields
            new_attr_names = new_attr_names or set()
            new_attr_names.update(selected_fields - model_field_names)
        annotated_fields = _get_annotated_fields_from_queryset_type(ctx.type)

    is_conflicting_attr_value = bool(
        # 1. Conflict with another symbol on the model (If not de-selected via a prior .values/.values_list call).
        # Ex:
        #     User.objects.prefetch_related(Prefetch(..., to_attr="id"))
        (model.typ.type.get(attr_name) and (deselected_fields is None or attr_name not in deselected_fields))
        # 2. Conflict with a previous annotation.
        # Ex:
        #     User.objects.annotate(foo=...).prefetch_related(Prefetch(...,to_attr="foo"))
        #     User.objects.prefetch_related(Prefetch(...,to_attr="foo")).prefetch_related(Prefetch(...,to_attr="foo"))
        or attr_name in annotated_fields
        # 3. Conflict with another symbol added in the current processing.
        # Ex:
        #     User.objects.prefetch_related(
        #        Prefetch("groups", Group.objects.filter(name="test"), to_attr="new_attr"),
        #        Prefetch("groups", Group.objects.all(), to_attr="new_attr"), # E: Not OK!
        #     )
        or (new_attr_names is not None and attr_name in new_attr_names)
    )
    if is_conflicting_attr_value:
        ctx.api.fail(
            f'Attribute "{attr_name}" already defined on "{model.typ}"',
            ctx.context,
            code=NO_REDEF,
        )
    return not is_conflicting_attr_value


def _extract_field_names_from_collection(
    ctx: MethodContext, django_context: DjangoContext, arg_index: int
) -> list[str] | None:
    if not (
        len(ctx.args) > arg_index
        and ctx.args[arg_index]
        and isinstance((collection_expr := ctx.args[arg_index][0]), (ListExpr, TupleExpr, SetExpr))
    ):
        return None

    return [
        field_name
        for field_arg in collection_expr.items
        if (field_name := helpers.resolve_string_attribute_value(field_arg, django_context)) is not None
    ]


def _extract_field_names_from_varargs(ctx: MethodContext) -> list[str]:
    return [
        lookup_value
        for lookup_type in (ctx.arg_types[0] if ctx.arg_types and ctx.arg_types[0] else [])
        if (lookup_value := helpers.get_literal_str_type(get_proper_type(lookup_type))) is not None
    ]


def _get_select_related_field_choices(model_cls: type[Model]) -> set[str]:
    """
    Get valid field choices for select_related lookups.
    Based on Django's SQLCompiler.get_related_selections._get_field_choices method.
    """
    opts = model_cls._meta

    # Direct relation fields (forward relations)
    direct_choices = (f.name for f in opts.fields if f.is_relation)

    # Reverse relation fields (backward relations with unique=True)
    reverse_choices = (f.field.related_query_name() for f in opts.related_objects if f.field.unique)
    return {*direct_choices, *reverse_choices}


def _validate_select_related_lookup(
    ctx: MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    lookup: str,
) -> bool:
    """Validate a single select_related lookup string."""
    if not lookup.strip():
        ctx.api.fail(
            f'Invalid field name "{lookup}" in select_related lookup',
            ctx.context,
        )
        return False

    lookup_parts = lookup.split(LOOKUP_SEP)
    observed_model = model_cls
    for i, part in enumerate(lookup_parts):
        valid_choices = _get_select_related_field_choices(observed_model)

        if part not in valid_choices:
            ctx.api.fail(
                f'Invalid field name "{part}" in select_related lookup. '
                f"Choices are: {', '.join(sorted(valid_choices)) or '(none)'}",
                ctx.context,
            )
            return False

        if i < len(lookup_parts) - 1:  # Not the last part
            try:
                field, observed_model = django_context.resolve_lookup_into_field(observed_model, part)
                if field is None:
                    return False
            except (FieldError, LookupsAreUnsupported):
                # For good measure, but we should never reach this since we already validated the part name
                return False

    return True


def validate_select_related(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Validates that all lookup strings passed to select_related() resolve to actual model fields and relations.

    Extracted and adapted from `django.db.models.sql.compiler.SQLCompiler.get_related_selections`
    """
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None:
        return ctx.default_return_type

    for lookup_value in _extract_field_names_from_varargs(ctx):
        _validate_select_related_lookup(ctx, django_context, django_model.cls, lookup_value)

    return ctx.default_return_type


def validate_bulk_update(
    ctx: MethodContext, django_context: DjangoContext, method: Literal["bulk_update", "abulk_update"]
) -> MypyType:
    """
    Type check the `fields` argument passed to `QuerySet.bulk_update(...)`.

    Extracted and adapted from `django.db.models.query.QuerySet.bulk_update`
    Mirrors tests from `django/tests/queries/test_bulk_update.py`
    """
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None or (
        field_names := _extract_field_names_from_collection(ctx, django_context, arg_index=1)
    ) is None:
        return ctx.default_return_type

    if not field_names:
        # Only error if the collection literal itself is empty (not when items are unresolvable).
        collection_expr = ctx.args[1][0]
        if isinstance(collection_expr, (ListExpr, TupleExpr, SetExpr)) and not collection_expr.items:
            ctx.api.fail(f'Field names must be given to "{method}()"', ctx.context)
        return ctx.default_return_type

    for field_name in field_names:
        validate_non_pk_concrete_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type


def _validate_bulk_create_unique_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, method: str
) -> bool:
    return (field := try_get_field(ctx, model_cls, field_name, resolve_pk=True)) is not None and check_field_concrete(
        ctx, field, field_name, method
    )


def validate_bulk_create(
    ctx: MethodContext, django_context: DjangoContext, method: Literal["bulk_create", "abulk_create"]
) -> MypyType:
    """
    Type check the `update_fields` and `unique_fields` arguments passed to `QuerySet.bulk_create(...)`.

    Extracted and adapted from `django.db.models.query.QuerySet._check_bulk_create_options`
    """
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None:
        return ctx.default_return_type

    update_field_names = _extract_field_names_from_collection(ctx, django_context, arg_index=4)
    if update_field_names is not None:
        for field_name in update_field_names:
            validate_non_pk_concrete_field(ctx, django_model.cls, field_name, method, attr_name="update_fields")

    unique_field_names = _extract_field_names_from_collection(ctx, django_context, arg_index=5)
    if unique_field_names is not None:
        for field_name in unique_field_names:
            _validate_bulk_create_unique_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type


def _validate_lookup(ctx: MethodContext, model_cls: type[Model], parts: list[str]) -> None:
    # Abstract models don't have a pk field, skip validation
    if model_cls._meta.abstract:
        return

    try:
        _, final_field, _, remainder = Query(model_cls).names_to_path(parts, model_cls._meta)
    except FieldError as exc:
        ctx.api.fail(exc.args[0], ctx.context)
        return

    # Check if the trailing part is a valid transform (e.g. __year, __month) on the field.
    # Transforms are allowed, but lookups (e.g. __exact) are not.
    if remainder and final_field.get_transform(remainder[0]) is None:
        msg = f"Cannot resolve keyword '{remainder[0]}' into field or transform on '{final_field.name}'."
        ctx.api.fail(msg, ctx.context)


def _validate_order_by_lookup(ctx: MethodContext, model_cls: type[Model], parts: list[str]) -> None:
    if len(parts) == 1 and parts[0] == "?":
        return

    _validate_lookup(ctx, model_cls, parts)


def validate_order_by(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None:
        return ctx.default_return_type

    selected_fields = _get_selected_fields_from_queryset_type(ctx.type) if isinstance(ctx.type, Instance) else None
    annotated_fields = _get_annotated_fields_from_queryset_type(ctx.type) if isinstance(ctx.type, Instance) else set()

    for lookup_value in _extract_field_names_from_varargs(ctx):
        parts = lookup_value.removeprefix("-").split(LOOKUP_SEP)

        if parts[0] in annotated_fields:
            # Skip validation for annotated fields
            continue
        if selected_fields is not None and parts[0] in selected_fields:
            # Skip validation for fields selected via values()/values_list()
            continue
        _validate_order_by_lookup(ctx, django_model.cls, parts)

    return ctx.default_return_type


def _validate_defer_only_fields(
    ctx: MethodContext, model_cls: type[Model], field_names: list[str], *, is_defer: bool
) -> None:
    if not is_defer and model_cls._meta.abstract:
        # Abstract models do not have a primary key field, but Query.add_immediate_loading()
        # assumes that one exists when resolving the "pk" alias.
        field_names = [field_name for field_name in field_names if field_name != "pk"]

    query = Query(model_cls)
    query.add_deferred_loading(field_names) if is_defer else query.add_immediate_loading(field_names)

    try:
        query.get_select_mask()
    except (FieldDoesNotExist, FieldError) as exc:
        method = "defer" if is_defer else "only"
        ctx.api.fail(f'Invalid field in "{method}()": {exc.args[0]}', ctx.context)


def validate_defer_only(ctx: MethodContext, django_context: DjangoContext, *, is_defer: bool) -> MypyType:
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None or not (
        field_names := _extract_field_names_from_varargs(ctx)
    ):
        return ctx.default_return_type

    _validate_defer_only_fields(ctx, django_model.cls, field_names, is_defer=is_defer)

    return ctx.default_return_type


def validate_distinct(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None:
        return ctx.default_return_type

    selected_fields = _get_selected_fields_from_queryset_type(ctx.type) if isinstance(ctx.type, Instance) else None
    annotated_fields = _get_annotated_fields_from_queryset_type(ctx.type) if isinstance(ctx.type, Instance) else set()

    raw_arg_types = ctx.arg_types[0] if ctx.arg_types and ctx.arg_types[0] else []
    raw_arg_count = len(raw_arg_types)
    field_lookups = _extract_field_names_from_varargs(ctx)
    for lookup_value in field_lookups:
        parts = lookup_value.split(LOOKUP_SEP)
        if parts[0] in annotated_fields:
            # Skip validation for annotated fields
            continue
        if selected_fields is not None and parts[0] in selected_fields:
            # Skip validation for fields selected via values()/values_list()
            continue
        _validate_lookup(ctx, django_model.cls, parts)

    # Replaces any earlier tag - Django replaces distinct_fields on each call, doesn't accumulate.
    default_return_type = get_proper_type(ctx.default_return_type)
    if isinstance(default_return_type, Instance):
        existing = default_return_type.extra_attrs
        new_attrs: dict[str, MypyType] | None = None
        if raw_arg_count == 1 and len(field_lookups) == 1 and LOOKUP_SEP not in field_lookups[0]:
            new_attrs = {f"{_DISTINCT_FIELD_ATTR_PREFIX}{field_lookups[0]}": AnyType(TypeOfAny.implementation_artifact)}
        elif raw_arg_count == 1 and not field_lookups and isinstance(get_proper_type(raw_arg_types[0]), AnyType):
            # Any could be the field being checked - don't flag errors hinging on an unknowable value.
            new_attrs = {_DISTINCT_FIELD_UNKNOWN_ATTR: AnyType(TypeOfAny.implementation_artifact)}
        updated = helpers.merge_extra_attrs(existing, new_attrs=new_attrs, drop_prefix=_DISTINCT_FIELD_ATTR_PREFIX)
        if existing is None or updated.attrs != existing.attrs:
            tagged = default_return_type.copy_modified()
            tagged.extra_attrs = updated
            return tagged

    return ctx.default_return_type


def gather_update_kwargs(ctx: MethodContext) -> dict[str, MypyType]:
    """Gather named arguments destined for the `**kwargs` collector."""
    kwargs: dict[str, MypyType] = {}
    named = (ARG_NAMED, ARG_NAMED_OPT)
    slots = zip(ctx.callee_arg_names, ctx.arg_kinds, ctx.arg_types, ctx.arg_names, strict=False)
    for formal_name, kinds, types, names in slots:
        for kind, arg_type, name in zip(kinds, types, names, strict=False):
            if kind in named and name is not None and name != formal_name:
                kwargs[name] = arg_type
    return kwargs


def validate_update(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    if (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None or not (
        kwargs := gather_update_kwargs(ctx)
    ):
        return ctx.default_return_type

    for field_name in kwargs:
        field = try_get_field(ctx, django_model.cls, field_name)
        if field is not None:
            check_field_concrete(ctx, field, field_name, method="update")

    return ctx.default_return_type


def validate_in_bulk(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    if (
        (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is None
        or (field_name_expr := helpers.get_call_argument_by_name(ctx, "field_name")) is None
        or (field_name := helpers.resolve_string_attribute_value(field_name_expr, django_context)) is None
        or field_name == "pk"
        or (field := try_get_field(ctx, django_model.cls, field_name)) is None
    ):
        return ctx.default_return_type

    if not (isinstance(ctx.type, Instance) and _is_distinct_on_field(ctx.type, field_name)):
        check_field_unique(ctx, django_model.cls, field, field_name, method="in_bulk")

    return ctx.default_return_type
