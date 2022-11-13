from collections.abc import Callable, Container
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

conditional_page: Callable[[_F], _F]

def require_http_methods(request_method_list: Container[str]) -> Callable[[_F], _F]: ...

require_GET: Callable[[_F], _F]
require_POST: Callable[[_F], _F]
require_safe: Callable[[_F], _F]

def condition(etag_func: Callable | None = ..., last_modified_func: Callable | None = ...) -> Callable: ...
def etag(etag_func: Callable[..., Any]) -> Callable[[_F], _F]: ...
def last_modified(last_modified_func: Callable[..., Any]) -> Callable[[_F], _F]: ...
