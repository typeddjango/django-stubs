from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


class LocaleMiddleware:
    def process_request(self, request: WSGIRequest) -> None: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponse
    ) -> HttpResponse: ...