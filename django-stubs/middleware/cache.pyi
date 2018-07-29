from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse,
    HttpResponseBase,
)
from typing import (
    Callable,
    Optional,
)


class CacheMiddleware:
    def __init__(self, get_response: None = ..., cache_timeout: Optional[int] = ..., **kwargs) -> None: ...


class FetchFromCacheMiddleware:
    def __init__(self, get_response: Optional[Callable] = ...) -> None: ...
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]: ...


class UpdateCacheMiddleware:
    def __init__(self, get_response: None = ...) -> None: ...
    def _should_update_cache(
        self,
        request: WSGIRequest,
        response: HttpResponse
    ) -> bool: ...
    def process_response(
        self,
        request: WSGIRequest,
        response: HttpResponseBase
    ) -> HttpResponseBase: ...