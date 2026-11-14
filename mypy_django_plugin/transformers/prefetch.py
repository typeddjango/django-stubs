"""Prefetching"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import FieldError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from mypy.errorcodes import NO_REDEF
from mypy.nodes import ARG_STAR, CallExpr, Expression
from mypy.types import AnyType, Instance, LiteralType, ProperType, TupleType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, LookupsAreUnsupported
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers.models import get_annotated_type
from mypy_django_plugin.transformers.querysets import check_valid_attr_value

if TYPE_CHECKING:
    from mypy.checker import TypeChecker
    from mypy.plugin import FunctionContext, MethodContext

    from mypy_django_plugin.lib.helpers import DjangoModel


def _infer_prefetch_queryset_type(queryset_expr: Expression, api: TypeChecker) -> Instance | None:
    """Infer the model Instance from `Prefetch(queryset=...)`"""
    qs_type = get_proper_type(api.get_expression_type(queryset_expr))
    if isinstance(qs_type, Instance):
        return qs_type
    return None


def _resolve_prefetch_string_argument(
    type_arg: MypyType,
    expr: Expression | None,
    django_context: DjangoContext,
    arg_name: str,
) -> str | None:
    # First try to get value from specialized type arg
    arg_value = helpers.get_literal_str_type(type_arg)
    if arg_value is not None:
        return arg_value

    # Fallback: parse inline call expression
    if isinstance(expr, CallExpr):
        arg_expr = helpers.get_class_init_argument_by_name(expr, arg_name)
        if arg_expr:
            return helpers.resolve_string_attribute_value(arg_expr, django_context)
    return None


def _resolve_prefetch_queryset_argument(
    type_arg: MypyType,
    expr: Expression | None,
    api: TypeChecker,
) -> Instance | None:
    # First try to get queryset type from specialized type arg
    queryset_type = get_proper_type(type_arg)
    if isinstance(queryset_type, Instance):
        elem_model = helpers.extract_model_type_from_queryset(queryset_type)
        # If we got a valid specific model type, return the queryset type
        if elem_model is not None and elem_model.type.fullname != fullnames.MODEL_CLASS_FULLNAME:
            return queryset_type

    # Fallback: parse inline call expression
    if isinstance(expr, CallExpr):
        queryset_expr = helpers.get_class_init_argument_by_name(expr, "queryset")
        if queryset_expr is not None:
            return _infer_prefetch_queryset_type(queryset_expr, api)

    return None


def _specialize_string_arg_to_literal(
    ctx: FunctionContext, django_context: DjangoContext, arg_name: str, fallback_type: MypyType
) -> MypyType:
    """
    Helper to specialize a string argument to a Literal[str] type.

    This allows the plugin to extract the actual string value for further processing
    and validation in later analysis phases.
    """

    if (arg_expr := helpers.get_call_argument_by_name(ctx, arg_name)) and (
        arg_value := helpers.resolve_string_attribute_value(arg_expr, django_context)
    ):
        api = helpers.get_typechecker_api(ctx)
        return LiteralType(value=arg_value, fallback=api.named_generic_type("builtins.str", []))

    return fallback_type


def specialize_prefetch_type(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    """Function hook for `Prefetch(...)` to specialize its `lookup` and `to_attr` generic parameters."""
    default = get_proper_type(ctx.default_return_type)
    if not isinstance(default, Instance):
        return ctx.default_return_type

    lookup_type = _specialize_string_arg_to_literal(ctx, django_context, "lookup", default.args[0])
    to_attr_type = _specialize_string_arg_to_literal(ctx, django_context, "to_attr", default.args[2])

    return default.copy_modified(args=[lookup_type, default.args[1], to_attr_type])


def gather_flat_args(ctx: MethodContext) -> list[tuple[Expression | None, ProperType]]:
    """
    Flatten all arguments into a uniform list of (expr, typ) pairs.

    This helper iterates over positional and named arguments and expands any starred
    arguments when their type is a TupleType with statically known items.
    """
    lookups: list[tuple[Expression | None, ProperType]] = []
    arg_start_idx = 0
    for expr, typ, kind in zip(ctx.args[0], ctx.arg_types[0], ctx.arg_kinds[0], strict=False):
        ptyp = get_proper_type(typ)
        if kind == ARG_STAR:
            # Expand starred tuple items if statically known
            if isinstance(ptyp, TupleType):
                lookups.append((None, get_proper_type(ptyp.items[arg_start_idx])))
            # If not a TupleType (e.g. list/Iterable), we cannot expand statically
            arg_start_idx += 1
            continue
        lookups.append((expr, ptyp))
    return lookups


def check_valid_prefetch_related_lookup(
    ctx: MethodContext,
    lookup: str,
    django_model: DjangoModel,
    django_context: DjangoContext,
    *,
    is_generic_prefetch: bool = False,
) -> bool:
    """Check if a lookup string resolve to something that can be prefetched"""
    current_model_cls = django_model.cls
    contenttypes_installed = django_context.apps_registry.is_installed("django.contrib.contenttypes")
    for through_attr in lookup.split(LOOKUP_SEP):
        rel_obj_descriptor = getattr(current_model_cls, through_attr, None)
        if rel_obj_descriptor is None:
            # If current_model_cls is "self", we cannot use `__name__` and want "self".
            model_name = getattr(current_model_cls, "__name__", current_model_cls)
            ctx.api.fail(
                (
                    f'Cannot find "{through_attr}" on "{model_name}" object, '
                    f'"{lookup}" is an invalid parameter to "prefetch_related()"'
                ),
                ctx.context,
            )
            return False
        if contenttypes_installed and is_generic_prefetch:
            try:
                from django.contrib.contenttypes.fields import GenericForeignKeyDescriptor
            except ImportError:  # Django < 6.1
                from django.contrib.contenttypes.fields import GenericForeignKey as GenericForeignKeyDescriptor  # type: ignore[assignment]

            if not isinstance(rel_obj_descriptor, GenericForeignKeyDescriptor):
                # If current_model_cls is "self", we cannot use `__name__` and want "self".
                model_name = getattr(current_model_cls, "__name__", current_model_cls)
                ctx.api.fail(
                    f'"{through_attr}" on "{model_name}" is not a GenericForeignKey, '
                    f"GenericPrefetch can only be used with GenericForeignKey fields",
                    ctx.context,
                )
                return True
        elif isinstance(rel_obj_descriptor, ForwardManyToOneDescriptor):
            current_model_cls = rel_obj_descriptor.field.remote_field.model
        elif isinstance(rel_obj_descriptor, ReverseOneToOneDescriptor):
            current_model_cls = rel_obj_descriptor.related.related_model
        elif isinstance(rel_obj_descriptor, ManyToManyDescriptor):
            current_model_cls = (
                rel_obj_descriptor.rel.related_model if rel_obj_descriptor.reverse else rel_obj_descriptor.rel.model
            )
        elif isinstance(rel_obj_descriptor, ReverseManyToOneDescriptor):
            if contenttypes_installed:
                from django.contrib.contenttypes.fields import ReverseGenericManyToOneDescriptor

                if isinstance(rel_obj_descriptor, ReverseGenericManyToOneDescriptor):
                    current_model_cls = rel_obj_descriptor.rel.model
                    continue
            current_model_cls = rel_obj_descriptor.rel.related_model
        else:
            if contenttypes_installed:
                try:
                    from django.contrib.contenttypes.fields import GenericForeignKeyDescriptor
                except ImportError:  # Django < 6.1
                    from django.contrib.contenttypes.fields import GenericForeignKey as GenericForeignKeyDescriptor  # type: ignore[assignment]

                if isinstance(rel_obj_descriptor, GenericForeignKeyDescriptor):
                    # Generic foreign keys can point to any model, so we use Model as the base type
                    return True
            ctx.api.fail(
                (
                    f'"{lookup}" does not resolve to an item that supports prefetching '
                    '- this is an invalid parameter to "prefetch_related()"'
                ),
                ctx.context,
            )
            return False
    return True


def check_conflicting_lookups(
    ctx: MethodContext,
    observed_attr: str,
    qs_types: dict[str, Instance | None],
    queryset_type: Instance | None,
) -> bool:
    is_conflicting_lookup = bool(observed_attr in qs_types and qs_types[observed_attr] != queryset_type)
    if is_conflicting_lookup:
        ctx.api.fail(
            f'Lookup "{observed_attr}" was already seen with a different queryset',
            ctx.context,
            code=NO_REDEF,
        )
    return is_conflicting_lookup


def extract_prefetch_related_annotations(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Extract annotated attributes via `prefetch_related(Prefetch(..., to_attr=...))`

    See https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-objects
    """
    api = helpers.get_typechecker_api(ctx)

    if not (
        isinstance(ctx.type, Instance)
        and isinstance((default_return_type := get_proper_type(ctx.default_return_type)), Instance)
        and (qs_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is not None
        and ctx.args
        and ctx.arg_types
        and ctx.arg_types[0]
        # Only process the correct overload, i.e.
        #     def prefetch_related(self, *lookups: str | Prefetch[_PrefetchedQuerySetT, _ToAttrT]) -> Self: ...
        and None not in ctx.callee_arg_names
    ):
        return ctx.default_return_type

    new_attrs: dict[str, MypyType] = {}  # A mapping of field_name / types to add to the model
    qs_types: dict[str, Instance | None] = {}  # A mapping of field_name / associated queryset type
    for expr, typ in gather_flat_args(ctx):
        if not (isinstance(typ, Instance) and typ.type.has_base(fullnames.PREFETCH_CLASS_FULLNAME)):
            # Handle plain string lookups (not Prefetch instances)
            lookup = helpers.get_literal_str_type(typ)
            queryset_type = None
            if lookup is not None:
                check_valid_prefetch_related_lookup(ctx, lookup, qs_model, django_context)
                check_conflicting_lookups(ctx, lookup, qs_types, queryset_type)
                qs_types[lookup] = queryset_type
            continue

        # 1) Extract lookup value from specialized type arg or call expression
        lookup = _resolve_prefetch_string_argument(typ.args[0], expr, django_context, "lookup")

        # 2) Extract to_attr value from specialized type arg or call expression
        to_attr = _resolve_prefetch_string_argument(typ.args[2], expr, django_context, "to_attr")
        if to_attr is None and lookup is None:
            continue

        # 3.a) Determine queryset type from specialized type arg or call expression
        queryset_type = _resolve_prefetch_queryset_argument(typ.args[1], expr, api)

        # 3.b) Extract model type from queryset type (or from the lookup value)
        elem_model: Instance | None = None
        if queryset_type is not None and isinstance(queryset_type, Instance):
            elem_model = helpers.extract_model_type_from_queryset(queryset_type)
        elif lookup:
            try:
                observed_model_cls = django_context.resolve_lookup_into_field(qs_model.cls, lookup)[1]
                if model_info := helpers.lookup_class_typeinfo(api, observed_model_cls):
                    elem_model = helpers.model_instance(model_info)
            except (FieldError, LookupsAreUnsupported):
                pass

        if to_attr and check_valid_attr_value(
            ctx, django_context, qs_model, to_attr, new_attr_names=set(new_attrs.keys())
        ):
            # When traversing multiple relations (e.g. "groups__user_set"), the to_attr is set
            # on the last item of the chain (e.g. Group), not on the root model (e.g. User).
            # We can't annotate an intermediate model from here, so skip adding the annotation
            # to the root model to avoid incorrectly attributing to_attr to it.
            if lookup and LOOKUP_SEP in lookup:
                continue
            new_attrs[to_attr] = api.named_generic_type(
                "builtins.list",
                [elem_model if elem_model is not None else AnyType(TypeOfAny.special_form)],
            )
            qs_types[to_attr] = queryset_type
        if not to_attr and lookup:
            check_valid_prefetch_related_lookup(
                ctx,
                lookup,
                qs_model,
                django_context,
                is_generic_prefetch=typ.type.has_base(fullnames.GENERIC_PREFETCH_CLASS_FULLNAME),
            )
            check_conflicting_lookups(ctx, lookup, qs_types, queryset_type)
            qs_types[lookup] = queryset_type

    if not new_attrs:
        return ctx.default_return_type

    fields_dict = helpers.make_typeddict(api, new_attrs)

    annotated_model = get_annotated_type(api, qs_model.typ, fields_dict=fields_dict)

    # Keep row shape; if row is a model instance, update it to annotated
    # Todo: consolidate with `extract_proper_type_queryset_annotate` row handling above.
    if len(default_return_type.args) > 1:
        original_row = get_proper_type(default_return_type.args[1])
        row_type: MypyType = original_row
        if isinstance(original_row, Instance) and helpers.is_model_type(original_row.type):
            row_type = annotated_model
    else:
        row_type = annotated_model

    return default_return_type.copy_modified(args=[annotated_model, row_type])
