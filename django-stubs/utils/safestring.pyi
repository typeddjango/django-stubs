from typing import Any, Callable, TypeVar, overload

_SD = TypeVar("_SD", bound="SafeData")

class SafeData:
    def __html__(self: _SD) -> _SD: ...

class SafeString(str, SafeData):
    @overload
    def __add__(self, rhs: SafeString) -> SafeString: ...
    @overload
    def __add__(self, rhs: str) -> str: ...
    def __str__(self) -> str: ...

SafeText = SafeString

_C = TypeVar("_C", bound=Callable)

@overload
def mark_safe(s: _SD) -> _SD: ...
@overload
def mark_safe(s: _C) -> _C: ...
@overload
def mark_safe(s: Any) -> SafeString: ...
