from mypy.plugin import MethodContext
from mypy.types import AnyType, Instance, ProperType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers


def typecheck_queryset_filter(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    # Expected formal arguments for filter methods are `*args` and `**kwargs`. We'll only typecheck
    # `**kwargs`, which means that `arg_names[1]` is what we're interested in.

    lookup_kwargs = ctx.arg_names[1] if len(ctx.arg_names) >= 2 else []
    provided_lookup_types = ctx.arg_types[1] if len(ctx.arg_types) >= 2 else []

    if (
        not isinstance(ctx.type, Instance)
        or not ctx.type.args
        or not isinstance((model_type := get_proper_type(ctx.type.args[0])), Instance)
        or not helpers.is_model_type(model_type.type)
    ):
        return ctx.default_return_type

    api = helpers.get_typechecker_api(ctx)
    manager_info = ctx.type.type
    model_cls_fullname = helpers.get_manager_to_model(manager_info) or model_type.type.fullname
    model_info = helpers.lookup_fully_qualified_typeinfo(api, model_cls_fullname)
    if model_info is None:
        return ctx.default_return_type
    model_cls = (
        django_context.get_model_class_by_fullname(model_info.bases[0].type.fullname)
        if helpers.is_annotated_model(model_info)
        else django_context.get_model_class_by_fullname(model_cls_fullname)
    )
    if model_cls is None:
        return ctx.default_return_type

    for lookup_kwarg, provided_type in zip(lookup_kwargs, provided_lookup_types):
        if lookup_kwarg is None:
            continue
        provided_type = get_proper_type(provided_type)
        if isinstance(provided_type, Instance) and provided_type.type.has_base(
            fullnames.COMBINABLE_EXPRESSION_FULLNAME
        ):
            provided_type = resolve_combinable_type(provided_type, django_context)

        lookup_type: MypyType
        try:
            lookup_type = django_context.resolve_lookup_expected_type(ctx, model_cls, lookup_kwarg, model_type)
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

    return ctx.default_return_type


def resolve_combinable_type(combinable_type: Instance, django_context: DjangoContext) -> ProperType:
    if combinable_type.type.fullname != fullnames.F_EXPRESSION_FULLNAME:
        # Combinables aside from F expressions are unsupported
        return AnyType(TypeOfAny.explicit)

    return django_context.resolve_f_expression_type(combinable_type)
