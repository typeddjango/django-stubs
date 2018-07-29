from typing import (
    Callable,
    List,
)


def condition(etag_func: Callable = ..., last_modified_func: None = ...) -> Callable: ...


def etag(etag_func: Callable) -> Callable: ...


def require_http_methods(request_method_list: List[str]) -> Callable: ...