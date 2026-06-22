from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import FieldDoesNotExist

if TYPE_CHECKING:
    from django.db.models.base import Model
    from django.db.models.options import _AnyField
    from mypy.plugin import MethodContext


def try_get_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, *, resolve_pk: bool = False
) -> _AnyField | None:
    opts = model_cls._meta
    resolved_name = opts.pk.name if resolve_pk and field_name == "pk" else field_name
    try:
        return opts.get_field(resolved_name)
    except FieldDoesNotExist as e:
        ctx.api.fail(str(e), ctx.context)
        return None


def check_field_concrete(ctx: MethodContext, field: _AnyField, field_name: str, method: str) -> bool:
    if not field.concrete or field.many_to_many:
        ctx.api.fail(f'"{method}()" can only be used with concrete fields. Got "{field_name}"', ctx.context)
        return False
    return True


def check_field_not_pk(
    ctx: MethodContext,
    model_cls: type[Model],
    field: _AnyField,
    field_name: str,
    method: str,
    *,
    attr_name: str | None = None,
) -> bool:
    opts = model_cls._meta
    all_pk_fields = set(getattr(opts, "pk_fields", [opts.pk]))
    for parent in getattr(opts, "all_parents", opts.get_parent_list()):
        all_pk_fields.update(getattr(parent._meta, "pk_fields", [parent._meta.pk]))
    if field in all_pk_fields:
        param_str = f' in "{attr_name}="' if attr_name else ""
        ctx.api.fail(f'"{method}()" does not support primary key fields{param_str}. Got "{field_name}"', ctx.context)
        return False
    return True


def validate_non_pk_concrete_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, method: str, *, attr_name: str | None = None
) -> bool:
    """Check that ``field_name`` is a concrete, non-primary-key field of ``model_cls``.

    Mirrors Django's ``Options._non_pk_concrete_field_names``: the set of fields that may
    appear in a database ``UPDATE`` (e.g. ``bulk_update`` fields, ``save(update_fields=...)``).
    Foreign key attnames such as ``author_id`` are accepted.
    """
    return (
        (field := try_get_field(ctx, model_cls, field_name)) is not None
        and check_field_concrete(ctx, field, field_name, method)
        and check_field_not_pk(ctx, model_cls, field, field_name, method, attr_name=attr_name)
    )
