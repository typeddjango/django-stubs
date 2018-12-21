from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

re_accepts_gzip: Any

class GZipMiddleware(MiddlewareMixin):
    def process_response(self, request: WSGIRequest, response: HttpResponseBase) -> HttpResponseBase: ...
