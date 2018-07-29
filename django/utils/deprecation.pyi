from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from typing import (
    Callable,
    Optional,
    Type,
)


class MiddlewareMixin:
    def __call__(self, request: WSGIRequest) -> HttpResponseBase: ...
    def __init__(self, get_response: Optional[Callable] = ...) -> None: ...


class warn_about_renamed_method:
    def __call__(self, f: Callable) -> Callable: ...
    def __init__(
        self,
        class_name: str,
        old_method_name: str,
        new_method_name: str,
        deprecation_warning: Type[DeprecationWarning]
    ) -> None: ...