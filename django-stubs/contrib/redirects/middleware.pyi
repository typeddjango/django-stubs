from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class RedirectFallbackMiddleware(MiddlewareMixin):
    response_gone_class: Any = ...
    response_redirect_class: Any = ...
    def process_response(self, request: WSGIRequest, response: HttpResponse) -> HttpResponse: ...
