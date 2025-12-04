from typing import TYPE_CHECKING

from django.utils.csp import CSP as CSP

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from django.utils.deprecation import MiddlewareMixin

class CSPMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None: ...
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse: ...
