from csrf_tests.tests import TestingHttpRequest
from django.http.request import HttpRequest
from typing import (
    Any,
    Callable,
    Dict,
    Tuple,
)


def csrf_exempt(view_func: Callable) -> Callable: ...


class _EnsureCsrfCookie:
    def _reject(self, request: TestingHttpRequest, reason: str) -> None: ...
    def process_view(
        self,
        request: TestingHttpRequest,
        callback: Callable,
        callback_args: Tuple,
        callback_kwargs: Dict[Any, Any]
    ) -> None: ...


class _EnsureCsrfToken:
    def _reject(self, request: HttpRequest, reason: str) -> None: ...