# Stubs for django.conf.urls (Python 3.5)

from typing import Any, Callable, Dict, List, Optional, overload, Tuple, Union

from django.http.response import HttpResponse
from django.urls import (
    RegexURLPattern, RegexURLResolver
)
from django.urls.resolvers import URLConf

handler400 = ...  # type: str
handler403 = ...  # type: str
handler404 = ...  # type: str
handler500 = ...  # type: str

def include(arg: Any, namespace: str=None, app_name: str=None) -> Tuple[URLConf, Optional[str], Optional[str]]: ...

@overload
def url(regex: str, view: Callable[..., HttpResponse], kwargs: Dict[str, Any]=None, name: str=None) -> RegexURLPattern: ...  # type: ignore  # issue 253 of typing
@overload
def url(regex: str, view: Tuple[URLConf, Optional[str], Optional[str]], kwargs: Dict[str, Any]=None, name: str=None) -> RegexURLResolver: ...
@overload
def url(regex: str, view: List[Union[URLConf, str]], kwargs: Dict[str, Any]=None, name: str=None) -> RegexURLResolver: ...
