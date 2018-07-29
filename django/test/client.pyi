from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.wsgi import WSGIRequest
from django.dispatch.dispatcher import Signal
from django.http.request import (
    HttpRequest,
    QueryDict,
)
from django.http.response import (
    FileResponse,
    HttpResponse,
    HttpResponseBase,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.template.base import Template
from django.template.context import Context
from django.test.utils import ContextList
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)
from urllib.parse import ParseResult


def closing_iterator_wrapper(iterable: map, close: Callable) -> None: ...


def conditional_content_removal(
    request: HttpRequest,
    response: HttpResponseBase
) -> HttpResponseBase: ...


def encode_file(boundary: str, key: str, file: object) -> List[bytes]: ...


def encode_multipart(boundary: str, data: Dict[str, Any]) -> bytes: ...


def store_rendered_templates(
    store: Dict[str, Union[List[Template], ContextList]],
    signal: Signal,
    sender: Template,
    template: Template,
    context: Context,
    **kwargs
) -> None: ...


class Client:
    def __init__(self, enforce_csrf_checks: bool = ..., **defaults) -> None: ...
    def _handle_redirects(
        self,
        response: Union[HttpResponseForbidden, HttpResponseRedirect],
        data: Any = ...,
        content_type: str = ...,
        **extra
    ) -> HttpResponse: ...
    def _login(self, user: AbstractBaseUser, backend: Optional[str] = ...) -> None: ...
    def _parse_json(self, response: HttpResponse, **extra) -> Dict[str, Union[int, str]]: ...
    def delete(
        self,
        path: str,
        data: Union[str, Dict[str, str]] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def force_login(self, user: User, backend: Optional[str] = ...) -> None: ...
    def get(
        self,
        path: str,
        data: Optional[Union[Dict[str, str], QueryDict]] = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponseBase: ...
    def head(
        self,
        path: str,
        data: Optional[Dict[str, str]] = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def login(self, **credentials) -> bool: ...
    def logout(self) -> None: ...
    def options(
        self,
        path: str,
        data: Union[str, Dict[str, str]] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def patch(
        self,
        path: str,
        data: Union[str, Dict[str, str]] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def post(
        self,
        path: str,
        data: Any = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def put(
        self,
        path: str,
        data: Union[str, bytes] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def request(self, **request): ...
    @property
    def session(self) -> SessionBase: ...
    def store_exc_info(self, **kwargs) -> None: ...
    def trace(
        self,
        path: str,
        data: Dict[str, str] = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...


class ClientHandler:
    def __call__(self, environ: Dict[str, Any]) -> HttpResponseBase: ...
    def __init__(self, enforce_csrf_checks: bool = ..., *args, **kwargs) -> None: ...


class FakePayload:
    def __init__(self, content: Optional[Union[str, bytes]] = ...) -> None: ...
    def __len__(self) -> int: ...
    def read(self, num_bytes: int = ...) -> bytes: ...
    def write(self, content: Union[str, bytes]) -> None: ...


class RequestFactory:
    def __init__(self, *, json_encoder = ..., **defaults) -> None: ...
    def _base_environ(self, **request) -> Dict[str, Any]: ...
    def _encode_data(self, data: Any, content_type: str) -> bytes: ...
    def _encode_json(self, data: Any, content_type: str) -> Any: ...
    def _get_path(self, parsed: ParseResult) -> str: ...
    def delete(
        self,
        path: str,
        data: Union[str, Dict[str, int]] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Union[str, bytes, Dict[str, str]] = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponseBase]: ...
    def get(
        self,
        path: str,
        data: Any = ...,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponse, FileResponse]: ...
    def head(
        self,
        path: str,
        data: Optional[Dict[str, str]] = ...,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponse]: ...
    def options(
        self,
        path: str,
        data: Dict[str, str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponseRedirect: ...
    def patch(
        self,
        path: str,
        data: str = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def post(
        self,
        path: str,
        data: Any = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponseBase]: ...
    def put(
        self,
        path: str,
        data: Union[str, Dict[str, str]] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra
    ) -> HttpResponse: ...
    def request(self, **request) -> WSGIRequest: ...
    def trace(
        self,
        path: str,
        secure: bool = ...,
        **extra
    ) -> Union[WSGIRequest, HttpResponse]: ...