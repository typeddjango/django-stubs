"""Annotations"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import ARG_NAMED, ARG_NAMED_OPT, ARG_POS, CallExpr, Decorator, Expression, StrExpr, Var
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    ProperType,
    TupleType,
    TypedDictType,
    TypeOfAny,
    TypeVarType,
    get_proper_type,
)
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import fullnames, helpers
from mypy_django_plugin.transformers.models import get_annotated_type
from mypy_django_plugin.transformers.querysets import check_valid_attr_value

if TYPE_CHECKING:
    from mypy.checker import TypeChecker
    from mypy.plugin import FunctionContext, MethodContext

    from mypy_django_plugin.django.context import DjangoContext


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


def _resolve_annotate_row_type(
    api: TypeChecker,
    default_return_type: Instance,
    annotated_model: ProperType,
    expression_types: dict[str, MypyType],
) -> MypyType:
    if len(default_return_type.args) <= 1:
        return annotated_model
    original_row_type = get_proper_type(default_return_type.args[1])
    if isinstance(original_row_type, TypedDictType):
        annotation_td = helpers.make_typeddict(
            api, {name: AnyType(TypeOfAny.from_omitted_generics) for name in expression_types}
        )
        return helpers.merge_typeddict(api, original_row_type, annotation_td)
    if isinstance(original_row_type, TupleType):
        if original_row_type.partial_fallback.type.has_base("typing.NamedTuple"):
            # Rebuild the NamedTuple with existing fields + annotation fields.
            annotation_fields = {name: AnyType(TypeOfAny.from_omitted_generics) for name in expression_types}
            return helpers.extend_oneoff_named_tuple(api, "Row", original_row_type, annotation_fields)
        return api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.from_omitted_generics)])
    if isinstance(original_row_type, Instance) and helpers.is_model_type(original_row_type.type):
        return annotated_model
    if isinstance(original_row_type, TypeVarType):
        upper_bound = get_proper_type(original_row_type.upper_bound)
        if isinstance(upper_bound, Instance) and helpers.is_model_type(upper_bound.type):
            return annotated_model
    return original_row_type


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
                    row_type = _resolve_annotate_row_type(api, default_return_type, upper_annotated, expression_types)
                    return default_return_type.copy_modified(args=[upper_annotated, row_type])
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

    row_type = _resolve_annotate_row_type(api, default_return_type, annotated_type, expression_types)
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
    new_args: list[MypyType] = [annotated_type]
    if len(default_return_type.args) > 1:
        original_row = get_proper_type(default_return_type.args[1])
        if isinstance(original_row, Instance) and helpers.is_model_type(original_row.type):
            new_args.append(annotated_type)
        else:
            new_args.append(default_return_type.args[1])
    else:
        new_args.append(annotated_type)
    return default_return_type.copy_modified(args=new_args)
