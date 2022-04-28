from io import BytesIO
from json import JSONEncoder
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    NoReturn,
    Optional,
    Pattern,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.http.cookie import SimpleCookie
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.template.base import Template
from django.urls import ResolverMatch

BOUNDARY: str = ...
MULTIPART_CONTENT: str = ...
CONTENT_TYPE_RE: Pattern = ...
JSON_CONTENT_TYPE_RE: Pattern = ...

class RedirectCycleError(Exception):
    last_response: HttpResponseBase = ...
    redirect_chain: List[Tuple[str, int]] = ...
    def __init__(self, message: str, last_response: HttpResponseBase) -> None: ...

class FakePayload:
    read_started: bool = ...
    def __init__(self, content: Optional[Union[bytes, str]] = ...) -> None: ...
    def __len__(self) -> int: ...
    def read(self, num_bytes: int = ...) -> bytes: ...
    def write(self, content: Union[bytes, str]) -> None: ...

_T = TypeVar("_T")

def closing_iterator_wrapper(iterable: Iterable[_T], close: Callable[[], Any]) -> Iterator[_T]: ...
def conditional_content_removal(request: HttpRequest, response: HttpResponseBase) -> HttpResponseBase: ...

class _WSGIResponse(HttpResponseBase):
    wsgi_request: WSGIRequest

class _ASGIResponse(HttpResponseBase):
    asgi_request: ASGIRequest

class ClientHandler(BaseHandler):
    enforce_csrf_checks: bool = ...
    def __init__(self, enforce_csrf_checks: bool = ..., *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, environ: Dict[str, Any]) -> _WSGIResponse: ...

class AsyncClientHandler(BaseHandler):
    enforce_csrf_checks: bool = ...
    def __init__(self, enforce_csrf_checks: bool = ..., *args: Any, **kwargs: Any) -> None: ...
    async def __call__(self, scope: Dict[str, Any]) -> _ASGIResponse: ...

def encode_multipart(boundary: str, data: Dict[str, Any]) -> bytes: ...
def encode_file(boundary: str, key: str, file: Any) -> List[bytes]: ...

class _RequestFactory(Generic[_T]):
    json_encoder: Type[JSONEncoder]
    defaults: Dict[str, str]
    cookies: SimpleCookie
    errors: BytesIO
    def __init__(self, *, json_encoder: Type[JSONEncoder] = ..., **defaults: Any) -> None: ...
    def request(self, **request: Any) -> _T: ...
    def get(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def post(self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def head(self, path: str, data: Any = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def trace(self, path: str, secure: bool = ..., **extra: Any) -> _T: ...
    def options(
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> _T: ...
    def put(self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def patch(self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def delete(self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any) -> _T: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Any = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> _T: ...

class RequestFactory(_RequestFactory[WSGIRequest]): ...

class _AsyncRequestFactory(_RequestFactory[_T]):
    def request(self, **request: Any) -> _T: ...
    def generic(
        self,
        method: str,
        path: str,
        data: Any = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> _T: ...

class AsyncRequestFactory(_AsyncRequestFactory[ASGIRequest]): ...

# fakes to distinguish WSGIRequest and ASGIRequest
class _MonkeyPatchedWSGIResponse(_WSGIResponse):
    def json(self) -> Any: ...
    request: Dict[str, Any]
    client: Client
    templates: List[Template]
    context: List[Dict[str, Any]]
    resolver_match: ResolverMatch

class _MonkeyPatchedASGIResponse(_ASGIResponse):
    def json(self) -> Any: ...
    request: Dict[str, Any]
    client: AsyncClient
    templates: List[Template]
    context: List[Dict[str, Any]]
    resolver_match: ResolverMatch

class ClientMixin:
    def store_exc_info(self, **kwargs: Any) -> None: ...
    def check_exception(self, response: HttpResponseBase) -> NoReturn: ...
    @property
    def session(self) -> SessionBase: ...
    def login(self, **credentials: Any) -> bool: ...
    def force_login(self, user: AbstractBaseUser, backend: Optional[str] = ...) -> None: ...
    def logout(self) -> None: ...

class Client(ClientMixin, _RequestFactory[_MonkeyPatchedWSGIResponse]):
    handler: ClientHandler
    raise_request_exception: bool
    exc_info: Optional[Tuple[Type[BaseException], BaseException, TracebackType]]
    def __init__(
        self, enforce_csrf_checks: bool = ..., raise_request_exception: bool = ..., **defaults: Any
    ) -> None: ...
    # Silence type warnings, since this class overrides arguments and return types in an unsafe manner.
    def request(self, **request: Any) -> _MonkeyPatchedWSGIResponse: ...
    def get(  # type: ignore
        self, path: str, data: Any = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def post(  # type: ignore
        self, path: str, data: Any = ..., content_type: str = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def head(  # type: ignore
        self, path: str, data: Any = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def trace(  # type: ignore
        self, path: str, data: Any = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def options(  # type: ignore
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        follow: bool = ...,
        secure: bool = ...,
        **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def put(  # type: ignore
        self, path: str, data: Any = ..., content_type: str = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def patch(  # type: ignore
        self, path: str, data: Any = ..., content_type: str = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...
    def delete(  # type: ignore
        self, path: str, data: Any = ..., content_type: str = ..., follow: bool = ..., secure: bool = ..., **extra: Any
    ) -> _MonkeyPatchedWSGIResponse: ...

class AsyncClient(ClientMixin, _AsyncRequestFactory[Awaitable[_MonkeyPatchedASGIResponse]]):
    handler: AsyncClientHandler
    raise_request_exception: bool
    exc_info: Any
    extra: Any
    def __init__(
        self, enforce_csrf_checks: bool = ..., raise_request_exception: bool = ..., **defaults: Any
    ) -> None: ...
    async def request(self, **request: Any) -> _MonkeyPatchedASGIResponse: ...
