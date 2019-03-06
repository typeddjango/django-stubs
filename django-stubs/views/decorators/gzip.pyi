from typing import Callable, TypeVar

_C = TypeVar("_C", bound=Callable)

def gzip_page(view_func: _C) -> _C: ...
