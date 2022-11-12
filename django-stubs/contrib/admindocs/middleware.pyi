from typing import Any, Callable, Dict, Tuple

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

class XViewMiddleware(MiddlewareMixin):
    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponseBase],
        view_args: Tuple,
        view_kwargs: Dict[Any, Any],
    ) -> HttpResponse | None: ...
