from collections.abc import Callable
from typing import Any

from django.core.cache import BaseCache
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase
from django.utils.deprecation import MiddlewareMixin

class UpdateCacheMiddleware(MiddlewareMixin):
    cache_timeout: float
    key_prefix: str
    cache_alias: str
    cache: BaseCache
    def process_response(self, request: HttpRequest, response: HttpResponseBase | str) -> HttpResponseBase | str: ...

class FetchFromCacheMiddleware(MiddlewareMixin):
    key_prefix: str
    cache_alias: str
    cache: BaseCache
    def process_request(self, request: HttpRequest) -> HttpResponse | None: ...

class CacheMiddleware(UpdateCacheMiddleware, FetchFromCacheMiddleware):
    key_prefix: str
    cache_alias: str
    cache_timeout: float
    cache: BaseCache
    def __init__(
        self,
        get_response: Callable = ...,
        cache_timeout: float | None = ...,
        page_timeout: float | None = ...,
        **kwargs: Any,
    ) -> None: ...
