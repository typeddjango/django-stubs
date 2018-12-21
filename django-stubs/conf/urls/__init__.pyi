# Stubs for django.conf.urls (Python 3.5)
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, overload, Tuple, Union

from django.http.response import HttpResponse
from django.urls import URLResolver, URLPattern

handler400 = ...  # type: str
handler403 = ...  # type: str
handler404 = ...  # type: str
handler500 = ...  # type: str

URLConf = Union[str, ModuleType]

def include(arg: Any, namespace: str = ..., app_name: str = ...) -> Tuple[URLConf, Optional[str], Optional[str]]: ...
@overload
def url(
    regex: str, view: Callable[..., HttpResponse], kwargs: Dict[str, Any] = ..., name: str = ...
) -> URLPattern: ...  # type: ignore  # issue 253 of typing
@overload
def url(
    regex: str, view: Tuple[URLConf, Optional[str], Optional[str]], kwargs: Dict[str, Any] = ..., name: str = ...
) -> URLResolver: ...
@overload
def url(regex: str, view: List[Union[URLConf, str]], kwargs: Dict[str, Any] = ..., name: str = ...) -> URLResolver: ...
