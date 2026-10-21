"""HTTP requests"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.types import Type as MypyType
from mypy.types import UninhabitedType, get_proper_type

if TYPE_CHECKING:
    from mypy.plugin import MethodContext


def check_querydict_is_mutable(ctx: MethodContext) -> MypyType:
    """Report mutations of immutable `QueryDict`s such as `request.GET`

    ```python
    request.GET["page"] = "2"  # error: This QueryDict is immutable.  [misc]
    params = request.GET.copy()
    params["page"] = "2"  # OK
    ```
    """
    ret_type = get_proper_type(ctx.default_return_type)
    if isinstance(ret_type, UninhabitedType):
        ctx.api.fail("This QueryDict is immutable.", ctx.context)
    return ctx.default_return_type
