# Stubs for django.conf.urls (Python 3.5)
from typing import Any, Callable, Dict, Sequence, Tuple, overload

from django.http.response import HttpResponse, HttpResponseBase
from django.urls import URLPattern, URLResolver
from django.urls import include as include

handler400: str | Callable[..., HttpResponse]
handler403: str | Callable[..., HttpResponse]
handler404: str | Callable[..., HttpResponse]
handler500: str | Callable[..., HttpResponse]

IncludedURLConf = Tuple[Sequence[URLResolver | URLPattern], str | None, str | None]

# Deprecated
@overload
def url(
    regex: str, view: Callable[..., HttpResponseBase], kwargs: Dict[str, Any] | None = ..., name: str | None = ...
) -> URLPattern: ...
@overload
def url(
    regex: str, view: IncludedURLConf, kwargs: Dict[str, Any] | None = ..., name: str | None = ...
) -> URLResolver: ...
@overload
def url(
    regex: str,
    view: Sequence[URLResolver | str],
    kwargs: Dict[str, Any] | None = ...,
    name: str | None = ...,
) -> URLResolver: ...
