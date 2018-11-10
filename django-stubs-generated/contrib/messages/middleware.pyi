from typing import Any, Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin


class MessageMiddleware(MiddlewareMixin):
    get_response: Callable
    def process_request(self, request: WSGIRequest) -> None: ...
    def process_response(
        self, request: HttpRequest, response: HttpResponseBase
    ) -> HttpResponseBase: ...
