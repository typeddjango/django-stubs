from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponseBase,
    HttpResponseNotFound,
    HttpResponsePermanentRedirect,
)
from typing import Optional


class BrokenLinkEmailsMiddleware:
    def is_ignorable_request(
        self,
        request: WSGIRequest,
        uri: str,
        domain: str,
        referer: str
    ) -> bool: ...
    def is_internal_request(self, domain: str, referer: str) -> bool: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponseNotFound
    ) -> HttpResponseNotFound: ...


class CommonMiddleware:
    def get_full_path_with_slash(self, request: WSGIRequest) -> str: ...
    def process_request(
        self,
        request: WSGIRequest
    ) -> Optional[HttpResponsePermanentRedirect]: ...
    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...
    def should_redirect_with_slash(self, request: WSGIRequest) -> bool: ...