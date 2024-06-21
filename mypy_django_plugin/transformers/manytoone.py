from typing import Optional

from mypy.plugin import MethodContext
from mypy.types import Instance
from mypy.types import Type as MypyType

from mypy_django_plugin.lib import fullnames, helpers


def get_model_of_related_manager(ctx: MethodContext) -> Optional[Instance]:
    """
    Returns the type parameter (_To) instance of a `RelatedManager` instance when it's a
    model. Otherwise `None` is returned.

    For example: if given a `RelatedManager[A]` where `A` is a model then `A` is
    returned.
    """
    if (
        isinstance(ctx.default_return_type, Instance)
        and ctx.default_return_type.type.fullname == fullnames.RELATED_MANAGER_CLASS
    ):
        # This is a call to '__get__' overload with a model instance of
        # 'ReverseManyToOneDescriptor'. Returning a 'RelatedManager'. Which we want to,
        # just like Django, build from the default manager of the related model.
        related_manager = ctx.default_return_type
        # Require first type argument of 'RelatedManager' to be a model
        if (
            len(related_manager.args) >= 1
            and isinstance(related_manager.args[0], Instance)
            and helpers.is_model_type(related_manager.args[0].type)
        ):
            return related_manager.args[0]

    return None


def refine_many_to_one_related_manager(ctx: MethodContext) -> MypyType:
    """
    Updates the 'RelatedManager' returned by e.g. 'ReverseManyToOneDescriptor' to be a subclass
    of 'RelatedManager' and the related model's default manager.
    """
    to_model_instance = get_model_of_related_manager(ctx)
    if to_model_instance is None:
        return ctx.default_return_type

    checker = helpers.get_typechecker_api(ctx)
    related_manager_info = helpers.get_reverse_manager_info(
        checker, to_model_instance.type, derived_from="_default_manager"
    )
    if related_manager_info is None:
        return ctx.default_return_type
    return Instance(related_manager_info, [])
