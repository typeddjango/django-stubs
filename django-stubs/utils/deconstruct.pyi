from typing import Any, Callable, Optional, TypeVar, overload

_T = TypeVar("_T")
_TCallable = TypeVar("_TCallable", bound=Callable[..., Any])

@overload
def deconstructible(_type: type[_T]) -> type[_T]: ...
@overload
def deconstructible(*, path: Optional[str] = ...) -> Callable[[_TCallable], _TCallable]: ...
