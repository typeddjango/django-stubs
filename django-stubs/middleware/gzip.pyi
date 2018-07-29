from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase


class GZipMiddleware:
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...