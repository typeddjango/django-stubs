from typing import Any, Callable, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

def gzip_page(view_func: _C) -> _C: ...
