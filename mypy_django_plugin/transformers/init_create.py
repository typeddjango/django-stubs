from django.db.models.base import Model
from mypy.errorcodes import CALL_ARG
from mypy.plugin import FunctionContext, MethodContext
from mypy.types import Instance, get_proper_type
from mypy.types import Type as MypyType

from mypy_django_plugin.django.context import DjangoContext
from mypy_django_plugin.lib import helpers


def get_actual_types(ctx: MethodContext | FunctionContext, expected_keys: list[str]) -> list[tuple[str, MypyType]]:
    actual_types = []
    # positionals
    for pos, (actual_name, actual_type) in enumerate(zip(ctx.arg_names[0], ctx.arg_types[0], strict=False)):
        if actual_name is None:
            if ctx.callee_arg_names[0] == "kwargs" or pos >= len(expected_keys):
                # unpacked dict as kwargs is not supported
                continue
            actual_name = expected_keys[pos]
        actual_types.append((actual_name, actual_type))
    # kwargs
    if len(ctx.callee_arg_names) > 1:
        for actual_name, actual_type in zip(ctx.arg_names[1], ctx.arg_types[1], strict=False):
            if actual_name is None:
                # unpacked dict as kwargs is not supported
                continue
            actual_types.append((actual_name, actual_type))
    return actual_types


def typecheck_model_method(
    ctx: FunctionContext | MethodContext,
    django_context: DjangoContext,
    model_cls: type[Model],
    method: str,
) -> None:
    """Type-checks positional and keyword arguments for Model methods like __init__(), create(), and acreate()."""
    typechecker_api = helpers.get_typechecker_api(ctx)
    expected_types = django_context.get_expected_types(typechecker_api, model_cls, method=method)
    expected_keys = [key for key in expected_types.keys() if key != "pk"]

    min_arg_count = helpers.get_min_argument_count(ctx)

    for actual_name, actual_type in get_actual_types(ctx, expected_keys):
        if actual_name not in expected_types:
            ctx.api.fail(f'Unexpected attribute "{actual_name}" for model "{model_cls.__name__}"', ctx.context)
            min_arg_count -= 1  # To avoid double error (Unexpected attribute + too many arguments)
            continue
        helpers.check_types_compatible(
            ctx,
            expected_type=expected_types[actual_name],
            actual_type=actual_type,
            error_message=f'Incompatible type for "{actual_name}" of "{model_cls.__name__}"',
        )

    if min_arg_count > len(expected_keys):
        ctx.api.fail(f'Too many arguments for "{model_cls.__name__}"', ctx.context, code=CALL_ARG)


def typecheck_model_init(ctx: FunctionContext, django_context: DjangoContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if (
        isinstance(default_return_type, Instance)
        and (model_cls := django_context.get_model_class_by_fullname(default_return_type.type.fullname)) is not None
    ):
        typecheck_model_method(ctx, django_context, model_cls, "__init__")

    return ctx.default_return_type


def typecheck_model_create(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if (
        isinstance(default_return_type, Instance)
        and (model_cls := django_context.get_model_class_by_fullname(default_return_type.type.fullname)) is not None
    ):
        typecheck_model_method(ctx, django_context, model_cls, "create")

    return ctx.default_return_type


def typecheck_model_acreate(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    default_return_type = get_proper_type(ctx.default_return_type)
    if (
        isinstance(default_return_type, Instance)
        # default_return_type at this point should be of type Coroutine[Any, Any, <Model>]
        and isinstance((model := get_proper_type(default_return_type.args[-1])), Instance)
        and (model_cls := django_context.get_model_class_by_fullname(model.type.fullname)) is not None
    ):
        typecheck_model_method(ctx, django_context, model_cls, "acreate")

    return ctx.default_return_type
