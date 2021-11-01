from typing import Any, Callable, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

def no_append_slash(view_func: _C) -> _C: ...
