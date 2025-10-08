from collections.abc import Sequence
from typing import Literal

from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db.models.base import Model
from django.db.models.fields.related import RelatedField
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from django.db.models.fields.reverse_related import ForeignObjectRel
from mypy.checker import TypeChecker
from mypy.errorcodes import NO_REDEF
from mypy.nodes import ARG_NAMED, ARG_NAMED_OPT, ARG_STAR, CallExpr, Expression, ListExpr, SetExpr, TupleExpr
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import AnyType, Instance, LiteralType, ProperType, TupleType, TypedDictType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, LookupsAreUnsupported
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.lib.helpers import DjangoModel
from mypy_django_plugin.transformers.models import get_annotated_type


def determine_proper_manager_type(ctx: FunctionContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    assert isinstance(default_return_type, Instance)

    outer_model_info = helpers.get_typechecker_api(ctx).scope.active_class()
    if (
        outer_model_info is None
        or not helpers.is_model_type(outer_model_info)
        or outer_model_info.self_type is None
        or not default_return_type.type.is_generic()
    ):
        return default_return_type

    return default_return_type.copy_modified(args=[outer_model_info.self_type])


def get_field_type_from_lookup(
    ctx: MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    *,
    method: str,
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
    if (isinstance(lookup_field, RelatedField) and lookup_field.column == lookup) or isinstance(
        lookup_field, ForeignObjectRel
    ):
        model_cls = django_context.get_field_related_model_cls(lookup_field)
        lookup_field = django_context.get_primary_key_field(model_cls)

    api = helpers.get_typechecker_api(ctx)
    model_info = helpers.lookup_class_typeinfo(api, model_cls)
    return django_context.get_field_get_type(api, model_info, lookup_field, method=method)


def get_values_list_row_type(
    ctx: MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    *,
    is_annotated: bool,
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
            lookup_type = get_field_type_from_lookup(
                ctx, django_context, model_cls, lookup=primary_key_field.attname, method="values_list"
            )
            assert lookup_type is not None
            return lookup_type
        if named:
            column_types: dict[str, MypyType] = {}
            for field in django_context.get_model_fields(model_cls):
                column_type = django_context.get_field_get_type(
                    typechecker_api, model_info, field, method="values_list"
                )
                column_types[field.attname] = column_type
            if is_annotated:
                # Return a NamedTuple with a fallback so that it's possible to access any field
                return helpers.make_oneoff_named_tuple(
                    typechecker_api,
                    "Row",
                    column_types,
                    extra_bases=[typechecker_api.named_generic_type(fullnames.ANY_ATTR_ALLOWED_CLASS_FULLNAME, [])],
                )
            return helpers.make_oneoff_named_tuple(typechecker_api, "Row", column_types)
        # flat=False, named=False, all fields
        if is_annotated:
            return typechecker_api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.special_form)])
        field_lookups = []
        for field in django_context.get_model_fields(model_cls):
            field_lookups.append(field.attname)

    if len(field_lookups) > 1 and flat:
        typechecker_api.fail("'flat' is not valid when 'values_list' is called with more than one field", ctx.context)
        return AnyType(TypeOfAny.from_error)

    column_types = {}
    for field_lookup in field_lookups:
        lookup_field_type = get_field_type_from_lookup(
            ctx, django_context, model_cls, lookup=field_lookup, method="values_list", silent_on_error=is_annotated
        )
        if lookup_field_type is None:
            if is_annotated:
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

    row_type = get_values_list_row_type(
        ctx, django_context, django_model.cls, is_annotated=django_model.is_annotated, flat=flat, named=named
    )
    ret = default_return_type.copy_modified(args=[django_model.typ, row_type])
    if not named and (field_lookups := resolve_field_lookups(ctx.args[0], django_context)):
        # For non-named values_list, the row type does not encode column names.
        # Attach selected field names to the returned QuerySet instance so that
        # subsequent annotate() can make an informed decision about name conflicts.
        ret.extra_attrs = helpers.merge_extra_attrs(ret.extra_attrs, new_immutable=set(field_lookups))
    return ret


def gather_kwargs(ctx: MethodContext) -> dict[str, MypyType] | None:
    num_args = len(ctx.arg_kinds)
    kwargs = {}
    named = (ARG_NAMED, ARG_NAMED_OPT)
    for i in range(num_args):
        if not ctx.arg_kinds[i]:
            continue
        if any(kind not in named for kind in ctx.arg_kinds[i]):
            # Only named arguments supported
            continue
        for j in range(len(ctx.arg_names[i])):
            name = ctx.arg_names[i][j]
            assert name is not None
            kwargs[name] = ctx.arg_types[i][j]
    return kwargs


def gather_expression_types(ctx: MethodContext) -> dict[str, MypyType]:
    kwargs = gather_kwargs(ctx)
    if not kwargs:
        return {}

    # For now, we don't try to resolve the output_field of the field would be, but use Any.
    # NOTE: It's important that we use 'special_form' for 'Any' as otherwise we can
    # get stuck with mypy interpreting an overload ambiguity towards the
    # overloaded 'Field.__get__' method when its 'model' argument gets matched. This
    # is because the model argument gets matched with a model subclass that is
    # parametrized with a type that contains the 'Any' below and then mypy runs in
    # to a (false?) ambiguity, due to 'Any', and can't decide what overload/return
    # type to select
    #
    # Example:
    #   class MyModel(models.Model):
    #       field = models.CharField()
    #
    #   # Our plugin auto generates the following subclass
    #   class MyModel_WithAnnotations(MyModel, django_stubs_ext.Annotations[_Annotations]):
    #       ...
    #   # Assume
    #   x = MyModel.objects.annotate(foo=F("id")).get()
    #   reveal_type(x)  # MyModel_WithAnnotations[TypedDict({"foo": Any})]
    #   # Then, on an attribute access of 'field' like
    #   reveal_type(x.field)
    #
    # Now 'CharField.__get__', which is overloaded, is passed 'x' as the 'model'
    # argument and mypy consider it ambiguous to decide which overload method to
    # select due to the 'Any' in 'TypedDict({"foo": Any})'. But if we specify the
    # 'Any' as 'TypeOfAny.special_form' mypy doesn't consider the model instance to
    # contain 'Any' and the ambiguity goes away.
    return {name: AnyType(TypeOfAny.special_form) for name, _ in kwargs.items()}


def extract_proper_type_queryset_annotate(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return AnyType(TypeOfAny.from_omitted_generics)

    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        return ctx.default_return_type

    api = helpers.get_typechecker_api(ctx)

    expression_types = {
        attr_name: typ
        for attr_name, typ in gather_expression_types(ctx).items()
        if check_valid_attr_value(ctx, django_context, django_model, attr_name)
    }

    annotated_type: ProperType = django_model.typ
    if expression_types:
        fields_dict = helpers.make_typeddict(
            api,
            fields=expression_types,
            required_keys=set(expression_types.keys()),
            readonly_keys=set(),
        )
        annotated_type = get_annotated_type(api, django_model.typ, fields_dict=fields_dict)

    row_type: MypyType
    if len(default_return_type.args) > 1:
        original_row_type = get_proper_type(default_return_type.args[1])
        row_type = original_row_type
        if isinstance(original_row_type, TypedDictType):
            row_type = api.named_generic_type(
                "builtins.dict", [api.named_generic_type("builtins.str", []), AnyType(TypeOfAny.from_omitted_generics)]
            )
        elif isinstance(original_row_type, TupleType):
            if original_row_type.partial_fallback.type.has_base("typing.NamedTuple"):
                # TODO: Use a NamedTuple which contains the known fields, but also
                #  falls back to allowing any attribute access.
                row_type = AnyType(TypeOfAny.implementation_artifact)
            else:
                row_type = api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.from_omitted_generics)])
        elif isinstance(original_row_type, Instance) and helpers.is_model_type(original_row_type.type):
            row_type = annotated_type
    else:
        row_type = annotated_type
    return default_return_type.copy_modified(args=[annotated_type, row_type])


def resolve_field_lookups(lookup_exprs: Sequence[Expression], django_context: DjangoContext) -> list[str] | None:
    field_lookups = []
    for field_lookup_expr in lookup_exprs:
        field_lookup = helpers.resolve_string_attribute_value(field_lookup_expr, django_context)
        if field_lookup is None:
            return None
        field_lookups.append(field_lookup)
    return field_lookups


def extract_proper_type_queryset_values(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Extract proper return type for QuerySet.values(*fields, **expressions) method calls.

    See https://docs.djangoproject.com/en/5.2/ref/models/querysets/#values
    """
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None or django_model.is_annotated:
        return ctx.default_return_type

    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        return ctx.default_return_type

    field_lookups = resolve_field_lookups(ctx.args[0], django_context)
    if field_lookups is None:
        return AnyType(TypeOfAny.from_error)

    # Bare `.values()` case
    if len(field_lookups) == 0 and not ctx.args[1]:
        for field in django_context.get_model_fields(django_model.cls):
            field_lookups.append(field.attname)

    column_types: dict[str, MypyType] = {}

    # Collect `*fields` types -- `.values("id", "name")`
    for field_lookup in field_lookups:
        field_lookup_type = get_field_type_from_lookup(
            ctx, django_context, django_model.cls, lookup=field_lookup, method="values"
        )
        if field_lookup_type is None:
            return default_return_type.copy_modified(args=[django_model.typ, AnyType(TypeOfAny.from_error)])

        column_types[field_lookup] = field_lookup_type

    # Collect `**expressions` types -- `.values(lower_name=Lower("name"), foo=F("name"))`
    column_types.update(gather_expression_types(ctx))
    row_type = helpers.make_typeddict(ctx.api, column_types, set(column_types.keys()), set())
    return default_return_type.copy_modified(args=[django_model.typ, row_type])


def _infer_prefetch_queryset_type(queryset_expr: Expression, api: TypeChecker) -> Instance | None:
    """Infer the model Instance from `Prefetch(queryset=...)`"""
    try:
        qs_type = get_proper_type(api.expr_checker.accept(queryset_expr))
    except Exception:
        return None
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
        elem_model = helpers.extract_model_type_from_queryset(queryset_type, api)
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

    if arg_expr := helpers.get_call_argument_by_name(ctx, arg_name):
        if arg_value := helpers.resolve_string_attribute_value(arg_expr, django_context):
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


def _get_selected_fields_from_queryset_type(qs_type: Instance) -> set[str] | None:
    """
    Derive selected field names from a QuerySet type.

    Sources:
      - values(): encoded in the row TypedDict keys
      - values_list(named=True): row is a NamedTuple; extract field names from fallback TypeInfo
      - values_list(named=False): stored in qs_type.extra_attrs.immutable
    """
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
    if isinstance(ctx.type, Instance):
        selected_fields = _get_selected_fields_from_queryset_type(ctx.type)
        if selected_fields is not None:
            model_field_names = {f.name for f in django_context.get_model_fields(model.cls)}
            deselected_fields = model_field_names - selected_fields
            new_attr_names = new_attr_names or set()
            new_attr_names.update(selected_fields - model_field_names)

    is_conflicting_attr_value = bool(
        # 1. Conflict with another symbol on the model (If not de-selected via a prior .values/.values_list call).
        # Ex:
        #     User.objects.prefetch_related(Prefetch(..., to_attr="id"))
        (model.typ.type.get(attr_name) and (deselected_fields is None or attr_name not in deselected_fields))
        # 2. Conflict with a previous annotation.
        # Ex:
        #     User.objects.annotate(foo=...).prefetch_related(Prefetch(...,to_attr="foo"))
        #     User.objects.prefetch_related(Prefetch(...,to_attr="foo")).prefetch_related(Prefetch(...,to_attr="foo"))
        or (model.typ.extra_attrs and attr_name in model.typ.extra_attrs.attrs)
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
    for through_attr in lookup.split("__"):
        rel_obj_descriptor = getattr(current_model_cls, through_attr, None)
        if rel_obj_descriptor is None:
            ctx.api.fail(
                (
                    f'Cannot find "{through_attr}" on "{current_model_cls.__name__}" object, '
                    f'"{lookup}" is an invalid parameter to "prefetch_related()"'
                ),
                ctx.context,
            )
            return False
        if contenttypes_installed and is_generic_prefetch:
            from django.contrib.contenttypes.fields import GenericForeignKey

            if not isinstance(rel_obj_descriptor, GenericForeignKey):
                ctx.api.fail(
                    f'"{through_attr}" on "{current_model_cls.__name__}" is not a GenericForeignKey, '
                    f"GenericPrefetch can only be used with GenericForeignKey fields",
                    ctx.context,
                )
                return True
        elif isinstance(rel_obj_descriptor, ForwardManyToOneDescriptor):
            current_model_cls = rel_obj_descriptor.field.remote_field.model
        elif isinstance(rel_obj_descriptor, ReverseOneToOneDescriptor):
            current_model_cls = rel_obj_descriptor.related.related_model  # type:ignore[assignment] # Can't be 'self' for non abstract models
        elif isinstance(rel_obj_descriptor, ManyToManyDescriptor):
            current_model_cls = (
                rel_obj_descriptor.rel.related_model if rel_obj_descriptor.reverse else rel_obj_descriptor.rel.model  # type:ignore[assignment] # Can't be 'self' for non abstract models
            )
        elif isinstance(rel_obj_descriptor, ReverseManyToOneDescriptor):
            if contenttypes_installed:
                from django.contrib.contenttypes.fields import ReverseGenericManyToOneDescriptor

                if isinstance(rel_obj_descriptor, ReverseGenericManyToOneDescriptor):
                    current_model_cls = rel_obj_descriptor.rel.model
                    continue
            current_model_cls = rel_obj_descriptor.rel.related_model  # type:ignore[assignment] # Can't be 'self' for non abstract models
        else:
            if contenttypes_installed:
                from django.contrib.contenttypes.fields import GenericForeignKey

                if isinstance(rel_obj_descriptor, GenericForeignKey):
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

    See https://docs.djangoproject.com/en/5.2/ref/models/querysets/#prefetch-objects
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
            elem_model = helpers.extract_model_type_from_queryset(queryset_type, api)
        elif lookup:
            try:
                observed_model_cls = django_context.resolve_lookup_into_field(qs_model.cls, lookup)[1]
                if model_info := helpers.lookup_class_typeinfo(api, observed_model_cls):
                    elem_model = Instance(model_info, [])
            except (FieldError, LookupsAreUnsupported):
                pass

        if to_attr and check_valid_attr_value(
            ctx, django_context, qs_model, to_attr, new_attr_names=set(new_attrs.keys())
        ):
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

    fields_dict = helpers.make_typeddict(
        api,
        fields=new_attrs,
        required_keys=set(new_attrs.keys()),
        readonly_keys=set(),
    )

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

    lookup_parts = lookup.split("__")
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
    if not (
        isinstance(ctx.type, Instance)
        and (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is not None
        and ctx.arg_types
        and ctx.arg_types[0]
    ):
        return ctx.default_return_type

    for lookup_type in ctx.arg_types[0]:
        lookup_value = helpers.get_literal_str_type(get_proper_type(lookup_type))
        if lookup_value is not None:
            _validate_select_related_lookup(ctx, django_context, django_model.cls, lookup_value)

    return ctx.default_return_type


def _validate_bulk_update_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, method: Literal["bulk_update", "abulk_update"]
) -> bool:
    opts = model_cls._meta
    try:
        field = opts.get_field(field_name)
    except FieldDoesNotExist as e:
        ctx.api.fail(str(e), ctx.context)
        return False

    if not field.concrete or field.many_to_many:
        ctx.api.fail(f'"{method}()" can only be used with concrete fields. Got "{field_name}"', ctx.context)
        return False

    all_pk_fields = set(getattr(opts, "pk_fields", [opts.pk]))
    for parent in opts.all_parents:
        all_pk_fields.update(getattr(parent._meta, "pk_fields", [parent._meta.pk]))

    if field in all_pk_fields:
        ctx.api.fail(f'"{method}()" cannot be used with primary key fields. Got "{field_name}"', ctx.context)
        return False

    return True


def validate_bulk_update(
    ctx: MethodContext, django_context: DjangoContext, method: Literal["bulk_update", "abulk_update"]
) -> MypyType:
    """
    Type check the `fields` argument passed to `QuerySet.bulk_update(...)`.

    Extracted and adapted from `django.db.models.query.QuerySet.bulk_update`
    Mirrors tests from `django/tests/queries/test_bulk_update.py`
    """
    if not (
        isinstance(ctx.type, Instance)
        and (django_model := helpers.get_model_info_from_qs_ctx(ctx, django_context)) is not None
        and len(ctx.args) >= 2
        and ctx.args[1]
        and isinstance((fields_args := ctx.args[1][0]), (ListExpr, TupleExpr, SetExpr))
    ):
        return ctx.default_return_type

    if len(fields_args.items) == 0:
        ctx.api.fail(f'Field names must be given to "{method}()"', ctx.context)
        return ctx.default_return_type

    for field_arg in fields_args.items:
        field_name = helpers.resolve_string_attribute_value(field_arg, django_context)
        if field_name is not None:
            _validate_bulk_update_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type
