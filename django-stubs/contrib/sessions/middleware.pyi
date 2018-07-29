from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from typing import (
    Callable,
    Optional,
)


class SessionMiddleware:
    def __init__(self, get_response: Optional[Callable] = ...) -> None: ...
    def process_request(self, request: WSGIRequest) -> None: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...