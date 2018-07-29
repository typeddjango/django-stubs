from django.core.cache import DefaultCacheProxy
from django.core.cache.backends.locmem import LocMemCache
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    HttpResponse,
    HttpResponseBase,
    HttpResponseNotModified,
)
from typing import (
    List,
    Optional,
    Tuple,
    Union,
)


def _generate_cache_header_key(key_prefix: str, request: WSGIRequest) -> str: ...


def _generate_cache_key(
    request: WSGIRequest,
    method: str,
    headerlist: List[str],
    key_prefix: str
) -> str: ...


def _i18n_cache_key_suffix(request: WSGIRequest, cache_key: str) -> str: ...


def _if_match_passes(target_etag: Optional[str], etags: List[str]) -> bool: ...


def _if_modified_since_passes(last_modified: Optional[int], if_modified_since: int) -> bool: ...


def _if_none_match_passes(target_etag: Optional[str], etags: List[str]) -> bool: ...


def _if_unmodified_since_passes(last_modified: int, if_unmodified_since: int) -> bool: ...


def _not_modified(
    request: WSGIRequest,
    response: Optional[HttpResponse] = ...
) -> HttpResponseNotModified: ...


def _precondition_failed(request: WSGIRequest) -> HttpResponse: ...


def _to_tuple(s: str) -> Union[Tuple[str, str], Tuple[str, bool]]: ...


def add_never_cache_headers(response: HttpResponse) -> None: ...


def get_cache_key(
    request: WSGIRequest,
    key_prefix: Optional[str] = ...,
    method: str = ...,
    cache: Optional[Union[DefaultCacheProxy, backends.locmem.LocMemCache]] = ...
) -> Optional[str]: ...


def get_conditional_response(
    request: WSGIRequest,
    etag: Optional[str] = ...,
    last_modified: Optional[int] = ...,
    response: Optional[HttpResponse] = ...
) -> Optional[HttpResponse]: ...


def get_max_age(response: HttpResponse) -> Optional[int]: ...


def has_vary_header(response: HttpResponse, header_query: str) -> bool: ...


def learn_cache_key(
    request: WSGIRequest,
    response: HttpResponse,
    cache_timeout: Optional[Union[float, int]] = ...,
    key_prefix: Optional[str] = ...,
    cache: Optional[Union[DefaultCacheProxy, backends.locmem.LocMemCache]] = ...
) -> str: ...


def patch_cache_control(response: HttpResponseBase, **kwargs) -> None: ...


def patch_response_headers(response: HttpResponse, cache_timeout: int = ...) -> None: ...


def patch_vary_headers(
    response: HttpResponseBase,
    newheaders: Union[Tuple[str], Tuple[str, str]]
) -> None: ...


def set_response_etag(response: HttpResponse) -> HttpResponse: ...