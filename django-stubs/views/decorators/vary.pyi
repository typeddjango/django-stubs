import functools
from collections.abc import Callable
from typing import Any, TypeVar, cast

_F = TypeVar("_F", bound=Callable[..., Any])

def vary_on_headers(func: _F) -> _F: ...

# def vary_on_headers(*headers: Any) -> Callable[[_F], _F]:
#     def decorator(func: _F) -> _F:
#         @functools.wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             return func(*args, **kwargs)
#         return cast(_F, wrapper)
#     return decorator

def vary_on_cookie(func: _F) -> _F: ...
