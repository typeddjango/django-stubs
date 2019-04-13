from typing import Any, Callable, List, Optional, TypeVar

conditional_page: Any

def require_http_methods(request_method_list: List[str]) -> Callable: ...

require_GET: Any
require_POST: Any
require_safe: Any

_F = TypeVar("_F", bound=Callable[..., Any])

def condition(etag_func: Optional[Callable] = ..., last_modified_func: Optional[Callable] = ...) -> Callable: ...
def etag(etag_func: Callable[..., Any]) -> Callable[[_F], _F]: ...
def last_modified(last_modified_func: Callable[..., Any]) -> Callable[[_F], _F]: ...
