from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields.related import RelatedField
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
    ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor,
)
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.lookups import Transform
from django.db.models.sql.query import Query
from mypy.errorcodes import NO_REDEF
from mypy.nodes import (
    ARG_NAMED,
    ARG_NAMED_OPT,
    ARG_POS,
    ARG_STAR,
    CallExpr,
    Decorator,
    Expression,
    ListExpr,
    SetExpr,
    StrExpr,
    TupleExpr,
    Var,
)
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    LiteralType,
    ProperType,
    TupleType,
    TypedDictType,
    TypeOfAny,
    TypeVarType,
    get_proper_type,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext, LookupsAreUnsupported
from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers.models import get_annotated_type

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.db.models.base import Model
    from django.db.models.options import _AnyField
    from mypy.checker import TypeChecker
    from mypy.plugin import FunctionContext, MethodContext

    from mypy_django_plugin.lib.helpers import DjangoModel


def determine_proper_manager_type(ctx: FunctionContext) -> MypyType:
    """
    Fill the manager TypeVar on instantiation using the enclosing class.
    For example:

        class MyModel(Model):
            objects = MyManager()

    Is interpreted as:

        class MyModel(Model):
            objects: MyManager[MyModel] = MyManager()
    """
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
            method="values_list",
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
    ret = default_return_type.copy_modified(args=[django_model.typ, row_type])
    if not named and (field_lookups := resolve_field_lookups(ctx.args[0], django_context)):
        # For non-named values_list, the row type does not encode column names.
        # Attach selected field names to the returned QuerySet instance so that
        # subsequent annotate() can make an informed decision about name conflicts.
        ret.extra_attrs = helpers.merge_extra_attrs(ret.extra_attrs, new_immutable=set(field_lookups))
    return ret


def _aggregate_default_alias(expr: Expression, expr_type: MypyType) -> str | None:
    """Mirror `Aggregate.default_alias`: ``<source_expression>__<aggregate_name_lower>``.

    Django generates a default alias only for aggregates with a single source
    expression that has a `name`; complex expressions raise at runtime, so the
    plugin matches that and returns ``None`` for anything else.

    See https://docs.djangoproject.com/en/dev/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset
    """
    if not (
        isinstance(expr, CallExpr)
        and isinstance(proper := get_proper_type(expr_type), Instance)
        and proper.type.has_base(fullnames.AGGREGATE_CLASS_FULLNAME)
    ):
        return None
    source: Expression | None = None
    for arg, kind in zip(expr.args, expr.arg_kinds, strict=False):
        if kind != ARG_POS:
            continue
        if source is not None:
            return None
        source = arg
    # TODO: consider switching to `helpers.resolve_string_attribute_value` once
    # `gather_kwargs` threads `django_context` through — that would also handle
    # `Count(NAME_CONST)` and `Count(settings.X)`.
    if not isinstance(source, StrExpr):
        return None
    return f"{source.value}__{proper.type.name.lower()}"


def gather_kwargs(ctx: MethodContext) -> dict[str, MypyType] | None:
    kwargs: dict[str, MypyType] = {}
    named = (ARG_NAMED, ARG_NAMED_OPT)
    for slot in zip(ctx.arg_kinds, ctx.arg_types, ctx.arg_names, ctx.args, strict=False):
        for kind, arg_type, name, arg in zip(*slot, strict=False):
            if kind in named:
                assert name is not None
                kwargs[name] = arg_type
            elif kind == ARG_POS:
                alias = _aggregate_default_alias(arg, arg_type)
                if alias is not None:
                    kwargs[alias] = arg_type
    return kwargs


def reparameterize_func_output_field(ctx: FunctionContext) -> MypyType:
    """Reparameterize Func[_OutputField] from the output_field argument.

    When a generic Func subclass like Substr is nested directly inside a call with
    **kwargs: Any (e.g., QuerySet.annotate()), mypy infers _OutputField=Any because
    the target type is unconstrained. This hook corrects the return type by extracting
    the actual output_field argument type.
    """
    default = get_proper_type(ctx.default_return_type)
    if not isinstance(default, Instance) or not default.args:
        return ctx.default_return_type

    # Only act when the generic arg is Any (i.e., mypy didn't infer it)
    if not isinstance(get_proper_type(default.args[0]), AnyType):
        return ctx.default_return_type

    # Use the output_field argument type to fill the generic param
    output_field_type = helpers.get_call_argument_type_by_name(ctx, "output_field")
    if output_field_type is not None:
        field_type = get_proper_type(output_field_type)
        if isinstance(field_type, Instance):
            return default.copy_modified(args=[field_type])

    return ctx.default_return_type


def _resolve_output_field_type(expr_type: MypyType) -> MypyType | None:
    """Try to resolve the Python type for an expression's output_field.

    Handles multiple resolution strategies, in order of priority:
    1. Generic type args on the expression (e.g. Substr(output_field=BinaryField()) → bytes)
    2. ClassVar output_field declarations (e.g. Count.output_field: ClassVar[IntegerField] → int)
    3. @property/@cached_property output_field definitions (e.g. ArrayAgg → list[Any])

    Generic args take priority so that expressions like Substr(output_field=BinaryField())
    can override the default ClassVar[CharField] when a specific output field type is provided.
    """
    proper = get_proper_type(expr_type)
    if not isinstance(proper, Instance):
        return None

    # First, check generic type args for Field subclasses.
    # This supports the Generic[_OutputField] pattern (e.g., Subquery[IntegerField], Substr[BinaryField]).
    # Generic args take priority over ClassVar so that explicit type params override defaults.
    for arg in proper.args:
        arg_proper = get_proper_type(arg)
        if isinstance(arg_proper, Instance) and arg_proper.type.has_base(fullnames.FIELD_FULLNAME):
            type_args = helpers.get_field_type_args(arg_proper)
            if type_args is not None and not isinstance(type_args.get, AnyType):
                return type_args.get

    # Then check static output_field declarations (ClassVar or @property/@cached_property).
    output_field_sym = proper.type.get("output_field")
    if output_field_sym is None or output_field_sym.node is None:
        return None

    node = output_field_sym.node
    field_type: ProperType | None = None

    if isinstance(node, Var) and node.type is not None:
        field_type = get_proper_type(node.type)
    elif isinstance(node, Decorator) and node.var.is_property:
        func_type = node.func.type
        if isinstance(func_type, CallableType):
            field_type = get_proper_type(func_type.ret_type)

    if isinstance(field_type, Instance):
        result = helpers.get_private_descriptor_type(field_type.type, "_pyi_private_get_type", is_nullable=False)
        if not isinstance(get_proper_type(result), AnyType):
            return result

    return None


def gather_expression_types(ctx: MethodContext) -> dict[str, MypyType]:
    kwargs = gather_kwargs(ctx)
    if not kwargs:
        return {}

    # Try to resolve the output_field type for each expression. For expressions
    # with a static ClassVar output_field (e.g. Count → IntegerField → int),
    # we can infer the concrete Python type. Otherwise, fall back to Any.
    #
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
    result: dict[str, MypyType] = {}
    for name, expr_type in kwargs.items():
        resolved = _resolve_output_field_type(expr_type)
        if resolved is not None and not isinstance(get_proper_type(resolved), AnyType):
            result[name] = resolved
        else:
            result[name] = AnyType(TypeOfAny.special_form)
    return result


def _extract_model_type_var_upper_bound(ctx: MethodContext) -> Instance | None:
    """When the queryset's model type arg is a TypeVar bounded by a Model, return the upper bound."""
    if not isinstance(ctx.type, Instance):
        return None
    for base_type in [ctx.type, *ctx.type.type.bases]:
        if not len(base_type.args) or base_type.type.has_base(fullnames.MANY_RELATED_MANAGER):
            continue
        model = get_proper_type(base_type.args[0])
        if isinstance(model, TypeVarType):
            upper = get_proper_type(model.upper_bound)
            if isinstance(upper, Instance) and helpers.is_model_type(upper.type):
                return upper
    return None


def extract_proper_type_queryset_annotate(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        # When the queryset's model is a TypeVar (e.g. inside a generic queryset method body),
        # use the TypeVar's upper bound to build a temporary annotated type. This allows
        # `self.annotate(...)` to return `QS[Model@AnnotatedWith[...]]` which is compatible
        # with return types declared as `QS[WithAnnotations[_Model, ...]]`.
        upper_bound = _extract_model_type_var_upper_bound(ctx)
        if upper_bound is not None:
            default_return_type = get_proper_type(ctx.default_return_type)
            if isinstance(default_return_type, Instance):
                api = helpers.get_typechecker_api(ctx)
                expression_types = gather_expression_types(ctx)
                if expression_types:
                    fields_dict = helpers.make_typeddict(api, expression_types)
                    upper_annotated = get_annotated_type(api, upper_bound, fields_dict=fields_dict)
                    return default_return_type.copy_modified(args=[upper_annotated, upper_annotated])
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

    existing_row_extra_attrs: dict[str, MypyType] = {}
    if len(default_return_type.args) > 1:
        original_row_type = get_proper_type(default_return_type.args[1])
        if isinstance(original_row_type, Instance) and original_row_type.extra_attrs:
            existing_row_extra_attrs = dict(original_row_type.extra_attrs.attrs)

    all_fields = {**existing_row_extra_attrs, **expression_types}

    annotated_type: ProperType = django_model.typ
    if all_fields:
        fields_dict = helpers.make_typeddict(api, all_fields)
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
                # Rebuild the NamedTuple with existing fields + annotation fields.
                annotation_fields = {name: AnyType(TypeOfAny.from_omitted_generics) for name in expression_types}
                row_type = helpers.extend_oneoff_named_tuple(api, "Row", original_row_type, annotation_fields)
            else:
                row_type = api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.from_omitted_generics)])
        elif isinstance(original_row_type, Instance) and helpers.is_model_type(original_row_type.type):
            row_type = annotated_type
    else:
        row_type = annotated_type
    return default_return_type.copy_modified(args=[annotated_type, row_type])


def merge_annotations_from_custom_method(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    """
    Method hook for custom QuerySet/Manager methods that return annotated querysets.

    Ensures extra_attrs are set on annotated model Instances (so attribute access works)
    and merges annotations from the caller queryset with annotations from the return type.
    """
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return ctx.default_return_type

    default_return_type = get_proper_type(ctx.default_return_type)
    if not (
        isinstance(default_return_type, Instance)
        and (ret_model := helpers.extract_model_type_from_queryset(default_return_type))
        and helpers.is_annotated_model(ret_model.type)
        and ret_model.args
        and isinstance(new_td := get_proper_type(ret_model.args[0]), TypedDictType)
    ):
        return ctx.default_return_type

    api = helpers.get_typechecker_api(ctx)
    annotated_type = get_annotated_type(api, django_model.typ, fields_dict=new_td)
    return default_return_type.copy_modified(args=[annotated_type, annotated_type])


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
            method="values",
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
            from django.contrib.contenttypes.fields import GenericForeignKey

            if not isinstance(rel_obj_descriptor, GenericForeignKey):
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
                    elem_model = Instance(model_info, [])
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


def _try_get_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, *, resolve_pk: bool = False
) -> _AnyField | None:
    opts = model_cls._meta
    resolved_name = opts.pk.name if resolve_pk and field_name == "pk" else field_name
    try:
        return opts.get_field(resolved_name)
    except FieldDoesNotExist as e:
        ctx.api.fail(str(e), ctx.context)
        return None


def _check_field_concrete(ctx: MethodContext, field: _AnyField, field_name: str, method: str) -> bool:
    if not field.concrete or field.many_to_many:
        ctx.api.fail(f'"{method}()" can only be used with concrete fields. Got "{field_name}"', ctx.context)
        return False
    return True


def _check_field_not_pk(
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


def _validate_bulk_update_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, method: str, *, attr_name: str | None = None
) -> bool:
    return (
        (field := _try_get_field(ctx, model_cls, field_name)) is not None
        and _check_field_concrete(ctx, field, field_name, method)
        and _check_field_not_pk(ctx, model_cls, field, field_name, method, attr_name=attr_name)
    )


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
        _validate_bulk_update_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type


def _validate_bulk_create_unique_field(
    ctx: MethodContext, model_cls: type[Model], field_name: str, method: str
) -> bool:
    return (field := _try_get_field(ctx, model_cls, field_name, resolve_pk=True)) is not None and _check_field_concrete(
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
            _validate_bulk_update_field(ctx, django_model.cls, field_name, method, attr_name="update_fields")

    unique_field_names = _extract_field_names_from_collection(ctx, django_context, arg_index=5)
    if unique_field_names is not None:
        for field_name in unique_field_names:
            _validate_bulk_create_unique_field(ctx, django_model.cls, field_name, method)

    return ctx.default_return_type


def _validate_order_by_lookup(ctx: MethodContext, model_cls: type[Model], parts: list[str]) -> None:
    if len(parts) == 1 and parts[0] == "?":
        return

    # Abstract models don't have a pk field, skip validation
    if model_cls._meta.abstract:
        return

    try:
        _, final_field, _, remainder = Query(model_cls).names_to_path(parts, model_cls._meta)
    except FieldError as exc:
        ctx.api.fail(exc.args[0], ctx.context)
        return

    if remainder:
        # Check if the trailing part is a valid transform (e.g. __year, __month) on the field.
        # Transforms are allowed in order_by, but lookups (e.g. __exact) are not.
        lookup_cls = final_field.get_lookups().get(remainder[0])
        if lookup_cls is None or not issubclass(lookup_cls, Transform):
            msg = f"Cannot resolve keyword '{remainder[0]}' into field or transform on '{final_field.name}'."
            ctx.api.fail(msg, ctx.context)


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
