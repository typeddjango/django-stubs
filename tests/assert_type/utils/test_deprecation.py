from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.deprecation import MiddlewareMixin
from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from django.http import HttpRequest, HttpResponseBase


class MyMiddleware(MiddlewareMixin):
    @override
    def __call__(self, request: HttpRequest) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        return self.get_response(request)
