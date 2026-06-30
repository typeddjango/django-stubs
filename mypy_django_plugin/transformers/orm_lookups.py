from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import ARG_NAMED, DictExpr, StrExpr
from mypy.types import AnyType, Instance, ProperType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers

if TYPE_CHECKING:
    from mypy.plugin import MethodContext

    from mypy_django_plugin.django.context import DjangoContext


def typecheck_queryset_filter(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return ctx.default_return_type

    # We only typecheck the `**kwargs` formal parameter. Python's grammar guarantees
    # `**kwargs` is the last formal parameter when present, which holds for every
    # method this hook is registered for (`filter`, `get_or_create`, `update_or_create`, ...).
    lookup_kwargs = ctx.arg_names[-1]
    provided_lookup_types = ctx.arg_types[-1]

    for lookup_kwarg, provided_type in zip(lookup_kwargs, provided_lookup_types, strict=False):
        if lookup_kwarg is None:
            continue
        provided_type = get_proper_type(provided_type)
        if isinstance(provided_type, Instance) and provided_type.type.has_base(
            fullnames.COMBINABLE_EXPRESSION_FULLNAME
        ):
            provided_type = resolve_combinable_type(provided_type, django_context)

        lookup_type: MypyType
        try:
            lookup_type = django_context.resolve_lookup_expected_type(
                ctx, django_model.cls, lookup_kwarg, django_model.typ
            )
        except UnregisteredModelError:
            lookup_type = AnyType(TypeOfAny.from_error)
        # Managers as provided_type is not supported yet
        if isinstance(provided_type, Instance) and helpers.has_any_of_bases(
            provided_type.type, (fullnames.MANAGER_CLASS_FULLNAME, fullnames.QUERYSET_CLASS_FULLNAME)
        ):
            return ctx.default_return_type

        helpers.check_types_compatible(
            ctx,
            expected_type=lookup_type,
            actual_type=provided_type,
            error_message=f"Incompatible type for lookup {lookup_kwarg!r}:",
        )

    _typecheck_defaults_kwarg(ctx, django_model, django_context)

    return ctx.default_return_type


def _typecheck_defaults_kwarg(
    ctx: MethodContext, django_model: helpers.DjangoModel, django_context: DjangoContext
) -> None:
    """
    Validate `defaults=` and `create_defaults=` dict literals passed to
    `get_or_create` / `update_or_create` against the model's field setter
    types. Only literal `DictExpr` arguments with string-literal keys are
    checked; any other shape is silently skipped to avoid false positives.
    """
    defaults_positions = [
        idx for idx, name in enumerate(ctx.callee_arg_names) if name in ("defaults", "create_defaults")
    ]
    if not defaults_positions:
        return

    api = helpers.get_typechecker_api(ctx)
    expected_types = django_context.get_expected_types(api, django_model.cls, method="create")
    model_name = django_model.cls.__name__

    for idx in defaults_positions:
        if not ctx.args[idx]:
            continue
        if ctx.arg_kinds[idx][0] != ARG_NAMED:
            continue
        dict_expr = ctx.args[idx][0]
        if not isinstance(dict_expr, DictExpr):
            continue

        for key_expr, value_expr in dict_expr.items:
            if not isinstance(key_expr, StrExpr):
                continue
            key_name = key_expr.value
            if key_name not in expected_types:
                ctx.api.fail(
                    f'Unexpected attribute "{key_name}" for model "{model_name}"',
                    key_expr,
                )
                continue

            actual_type = api.get_expression_type(value_expr)
            helpers.check_types_compatible(
                ctx,
                expected_type=expected_types[key_name],
                actual_type=actual_type,
                error_message=f'Incompatible type for "{key_name}" of "{model_name}"',
            )


def resolve_combinable_type(combinable_type: Instance, django_context: DjangoContext) -> ProperType:
    if combinable_type.type.fullname != fullnames.F_EXPRESSION_FULLNAME:
        # Combinables aside from F expressions are unsupported
        return AnyType(TypeOfAny.explicit)

    return django_context.resolve_f_expression_type(combinable_type)
