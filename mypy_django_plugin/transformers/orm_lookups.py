from django.db.models.constants import LOOKUP_SEP
from mypy.plugin import MethodContext
from mypy.types import AnyType, Instance, LiteralType, ProperType, TypeOfAny, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.exceptions import UnregisteredModelError
from mypy_django_plugin.lib import fullnames, helpers


def _extract_literal_bool(provided_type: ProperType) -> bool | None:
    literal: LiteralType | None = None
    if isinstance(provided_type, LiteralType):
        literal = provided_type
    elif isinstance(provided_type, Instance) and provided_type.last_known_value is not None:
        literal = provided_type.last_known_value
    if literal is not None and isinstance(literal.value, bool):
        return literal.value
    return None


def typecheck_queryset_filter(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    django_model = helpers.get_model_info_from_qs_ctx(ctx, django_context)
    if django_model is None:
        return ctx.default_return_type

    # Expected formal arguments for filter methods are `*args` and `**kwargs`. We'll only typecheck
    # `**kwargs`, which means that `arg_names[1]` is what we're interested in.
    lookup_kwargs = ctx.arg_names[1] if len(ctx.arg_names) >= 2 else []
    provided_lookup_types = ctx.arg_types[1] if len(ctx.arg_types) >= 2 else []

    for lookup_kwarg, provided_type in zip(lookup_kwargs, provided_lookup_types, strict=False):
        if lookup_kwarg is None:
            continue
        provided_type = get_proper_type(provided_type)

        lookup_path, _, lookup_name = lookup_kwarg.rpartition(LOOKUP_SEP)

        if lookup_name == "isnull" and isinstance(provided_type, LiteralType):
            isnull_value = _extract_literal_bool(provided_type)

            if isnull_value is not None and lookup_path:
                field = None

                try:
                    real_model_cls = django_context.get_model_class_by_fullname(django_model.cls.fullname)
                    if real_model_cls is not None:
                        path_parts = lookup_path.split(LOOKUP_SEP)
                        current_model = real_model_cls

                        for part in path_parts:
                            field = current_model._meta.get_field(part)

                            if hasattr(field, "related_model") and field.related_model is not None:
                                current_model = field.related_model
                except Exception:
                    field = None

                if field is not None and getattr(field, "null", None) is False:
                    if isnull_value is True:
                        ctx.api.fail(
                            f'Field "{field.name}" does not allow NULL;'
                            f'using "__isnull=True" will always return an empty queryset.',
                            ctx.context,
                        )
                    elif isnull_value is False:
                        ctx.api.fail(
                            f'Field "{field.name}" does not allow NULL;'
                            f'using "__isnull=False" is a no-op and can be removed',
                            ctx.context,
                        )

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

    return ctx.default_return_type


def resolve_combinable_type(combinable_type: Instance, django_context: DjangoContext) -> ProperType:
    if combinable_type.type.fullname != fullnames.F_EXPRESSION_FULLNAME:
        # Combinables aside from F expressions are unsupported
        return AnyType(TypeOfAny.explicit)

    return django_context.resolve_f_expression_type(combinable_type)
