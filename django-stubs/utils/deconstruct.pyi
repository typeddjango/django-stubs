from collections.abc import Callable
from typing import Any, TypeVar, overload

_T = TypeVar("_T")
_TCallable = TypeVar("_TCallable", bound=Callable[..., Any])

@overload
def deconstructible(_type: type[_T]) -> type[_T]: ...
@overload
def deconstructible(*, path: str | None = ...) -> Callable[[_TCallable], _TCallable]: ...
