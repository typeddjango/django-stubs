from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.views import _ViewCallable

class XViewMiddleware(MiddlewareMixin):
    def process_view(
        self,
        request: HttpRequest,
        view_func: _ViewCallable,
        view_args: tuple[Any, ...],
        view_kwargs: dict[str, Any],
    ) -> HttpResponse | None: ...
