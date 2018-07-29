from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    HttpResponse,
    HttpResponsePermanentRedirect,
)
from typing import Optional


class SecurityMiddleware:
    def __init__(self, get_response: None = ...) -> None: ...
    def process_request(
        self,
        request: WSGIRequest
    ) -> Optional[HttpResponsePermanentRedirect]: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponse
    ) -> HttpResponse: ...