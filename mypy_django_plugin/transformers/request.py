from mypy.plugin import MethodContext
from mypy.types import Type as MypyType
from mypy.types import UninhabitedType, get_proper_type

from mypy_django_plugin.django.context import DjangoContext


def check_querydict_is_mutable(ctx: MethodContext, django_context: DjangoContext) -> MypyType:
    ret_type = get_proper_type(ctx.default_return_type)
    if isinstance(ret_type, UninhabitedType):
        ctx.api.fail("This QueryDict is immutable.", ctx.context)
    return ctx.default_return_type
