from collections.abc import Awaitable

from django.http import HttpRequest, HttpResponseBase
from django.utils.deprecation import MiddlewareMixin
from typing_extensions import override


class MyMiddleware(MiddlewareMixin):
    @override
    def __call__(self, request: HttpRequest) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        return self.get_response(request)
