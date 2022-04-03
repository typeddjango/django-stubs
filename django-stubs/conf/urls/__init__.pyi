# Stubs for django.conf.urls (Python 3.5)
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union, overload

from django.http.response import HttpResponse, HttpResponseBase
from django.urls import URLPattern, URLResolver
from django.urls import include as include

handler400: Union[str, Callable[..., HttpResponse]] = ...
handler403: Union[str, Callable[..., HttpResponse]] = ...
handler404: Union[str, Callable[..., HttpResponse]] = ...
handler500: Union[str, Callable[..., HttpResponse]] = ...

IncludedURLConf = Tuple[Sequence[Union[URLResolver, URLPattern]], Optional[str], Optional[str]]

# Deprecated
@overload
def url(
    regex: str, view: Callable[..., HttpResponseBase], kwargs: Optional[Dict[str, Any]] = ..., name: Optional[str] = ...
) -> URLPattern: ...
@overload
def url(
    regex: str, view: IncludedURLConf, kwargs: Optional[Dict[str, Any]] = ..., name: Optional[str] = ...
) -> URLResolver: ...
@overload
def url(
    regex: str,
    view: Sequence[Union[URLResolver, str]],
    kwargs: Optional[Dict[str, Any]] = ...,
    name: Optional[str] = ...,
) -> URLResolver: ...
