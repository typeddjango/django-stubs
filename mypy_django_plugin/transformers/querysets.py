from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.errorcodes import NO_REDEF
from mypy.types import Instance, TupleType, TypedDictType, get_proper_type

from mypy_django_plugin.lib import fullnames, helpers

if TYPE_CHECKING:
    from mypy.plugin import MethodContext

    from mypy_django_plugin.django.context import DjangoContext
    from mypy_django_plugin.lib.helpers import DjangoModel


def get_selected_fields_from_queryset_type(qs_type: Instance) -> set[str] | None:
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


def get_annotated_fields_from_queryset_type(qs_type: Instance) -> set[str]:
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
        selected_fields = get_selected_fields_from_queryset_type(ctx.type)
        if selected_fields is not None:
            model_field_names = {f.name for f in django_context.get_model_fields(model.cls)}
            deselected_fields = model_field_names - selected_fields
            new_attr_names = new_attr_names or set()
            new_attr_names.update(selected_fields - model_field_names)
        annotated_fields = get_annotated_fields_from_queryset_type(ctx.type)

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
