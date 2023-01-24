from collections.abc import Callable
from typing import Any, TypeVar, overload

_C = TypeVar("_C", bound=Callable[..., Any])

@overload
def staff_member_required(view_func: _C = ..., redirect_field_name: str | None = ..., login_url: str = ...) -> _C: ...
@overload
def staff_member_required(
    view_func: None = ..., redirect_field_name: str | None = ..., login_url: str = ...
) -> Callable[..., Any]: ...
