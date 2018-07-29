from django.http.request import HttpRequest
from django.http.response import HttpResponse


class XFrameOptionsMiddleware:
    def get_xframe_options_value(
        self,
        request: HttpRequest,
        response: HttpResponse
    ) -> str: ...
    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponse
    ) -> HttpResponse: ...