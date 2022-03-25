from typing import Any, Callable, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

gzip_page: Callable[[_C], _C] = ...
