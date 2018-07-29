from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


class ConditionalGetMiddleware:
    def needs_etag(self, response: HttpResponse) -> bool: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponse
    ) -> HttpResponse: ...