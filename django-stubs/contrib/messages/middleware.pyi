from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase


class MessageMiddleware:
    def process_request(self, request: WSGIRequest) -> None: ...
    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...