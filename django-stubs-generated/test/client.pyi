from datetime import date
from typing import Any, Callable, Dict, List, Optional, Union

from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.dispatch.dispatcher import Signal
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.template.base import Template
from django.template.context import Context
from django.test.utils import ContextList

class RedirectCycleError(Exception):
    last_response: django.http.response.HttpResponseRedirect = ...
    redirect_chain: List[Tuple[str, int]] = ...
    def __init__(self, message: str, last_response: HttpResponseRedirect) -> None: ...

class FakePayload:
    read_started: bool = ...
    def __init__(self, content: Optional[Union[bytes, str]] = ...) -> None: ...
    def __len__(self) -> int: ...
    def read(self, num_bytes: int = ...) -> bytes: ...
    def write(self, content: Union[bytes, str]) -> None: ...

class ClientHandler(BaseHandler):
    enforce_csrf_checks: bool = ...
    def __init__(self, enforce_csrf_checks: bool = ..., *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, environ: Dict[str, Any]) -> HttpResponseBase: ...

def encode_multipart(boundary: str, data: Dict[str, Any]) -> bytes: ...
def encode_file(boundary: str, key: str, file: Any) -> List[bytes]: ...

class RequestFactory:
    json_encoder: Type[django.core.serializers.json.DjangoJSONEncoder] = ...
    defaults: Dict[str, str] = ...
    cookies: http.cookies.SimpleCookie = ...
    errors: _io.BytesIO = ...
    def __init__(self, *, json_encoder: Any = ..., **defaults: Any) -> None: ...
    def request(self, **request: Any) -> WSGIRequest: ...
    def get(
        self, path: str, data: Optional[Union[Dict[str, date], QueryDict, str]] = ..., secure: bool = ..., **extra: Any
    ) -> Union[WSGIRequest, HttpResponseBase]: ...
    def post(
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> Union[WSGIRequest, HttpResponseBase]: ...
    def head(
        self, path: str, data: Optional[Union[Dict[str, str], str]] = ..., secure: bool = ..., **extra: Any
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def trace(self, path: str, secure: bool = ..., **extra: Any) -> Union[WSGIRequest, HttpResponse]: ...
    def options(
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def put(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], bytes, str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def patch(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def delete(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Union[Dict[str, str], bytes, str] = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Union[WSGIRequest, HttpResponseBase]: ...

class Client(RequestFactory):
    defaults: Dict[str, str]
    errors: _io.BytesIO
    json_encoder: Union[Type[django.core.serializers.json.DjangoJSONEncoder], unittest.mock.MagicMock]
    handler: django.test.client.ClientHandler = ...
    exc_info: None = ...
    def __init__(self, enforce_csrf_checks: bool = ..., **defaults: Any) -> None: ...
    def store_exc_info(self, **kwargs: Any) -> None: ...
    @property
    def session(self) -> SessionBase: ...
    def request(self, **request: Any) -> Any: ...
    def get(
        self,
        path: str,
        data: Optional[Union[Dict[str, Union[int, str]], QueryDict, str]] = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponseBase: ...
    def post(
        self, path: str, data: Any = ..., content_type: str = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponseBase: ...
    def head(
        self,
        path: str,
        data: Optional[Union[Dict[str, str], str]] = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def options(
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def put(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], bytes, str] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def patch(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], str] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def delete(
        self,
        path: str,
        data: Union[Dict[str, int], Dict[str, str], str] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> HttpResponse: ...
    def trace(
        self, path: str, data: Union[Dict[str, str], str] = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> HttpResponse: ...
    def login(self, **credentials: Any) -> bool: ...
    def force_login(self, user: User, backend: Optional[str] = ...) -> None: ...
    cookies: http.cookies.SimpleCookie = ...
    def logout(self) -> None: ...
