from typing import Any, Callable, Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RedirectFallbackMiddleware(MiddlewareMixin):
    get_response: Callable
    response_gone_class: Any = ...
    response_redirect_class: Any = ...
    def __init__(self, get_response: Optional[Callable] = ...) -> None: ...
    def process_response(
        self, request: WSGIRequest, response: HttpResponse
    ) -> HttpResponse: ...
