from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse,
    HttpResponseBase,
    HttpResponseForbidden,
)
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
)


def _compare_salted_tokens(request_csrf_token: str, csrf_token: str) -> bool: ...


def _get_failure_view() -> Callable: ...


def _get_new_csrf_string() -> str: ...


def _get_new_csrf_token() -> str: ...


def _salt_cipher_secret(secret: str) -> str: ...


def _sanitize_token(token: str) -> str: ...


def _unsalt_cipher_token(token: str) -> str: ...


def get_token(request: HttpRequest) -> str: ...


def rotate_token(request: HttpRequest) -> None: ...


class CsrfViewMiddleware:
    def _accept(self, request: HttpRequest) -> None: ...
    def _get_token(self, request: HttpRequest) -> Optional[str]: ...
    def _reject(
        self,
        request: HttpRequest,
        reason: str
    ) -> HttpResponseForbidden: ...
    def _set_token(self, request: HttpRequest, response: HttpResponse) -> None: ...
    def process_request(self, request: HttpRequest) -> None: ...
    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...
    def process_view(
        self,
        request: HttpRequest,
        callback: Callable,
        callback_args: Tuple,
        callback_kwargs: Dict[str, Any]
    ) -> Optional[HttpResponseForbidden]: ...