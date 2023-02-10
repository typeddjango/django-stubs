from collections.abc import Awaitable, Callable, Iterator, Mapping, Sequence
from typing import IO, Any, TypeVar

from django.core.handlers import base
from django.http.request import HttpRequest, _ImmutableQueryDict
from django.http.response import HttpResponseBase
from django.urls.resolvers import ResolverMatch, URLResolver
from django.utils.datastructures import MultiValueDict
from typing_extensions import TypeAlias

_ReceiveCallback: TypeAlias = Callable[[], Awaitable[Mapping[str, Any]]]

_SendCallback: TypeAlias = Callable[[Mapping[str, Any]], Awaitable[None]]

class ASGIRequest(HttpRequest):
    body_receive_timeout: int
    scope: Mapping[str, Any]
    resolver_match: ResolverMatch | None
    script_name: str | None
    path_info: str
    path: str
    method: str
    META: dict[str, Any]
    def __init__(self, scope: Mapping[str, Any], body_file: IO[bytes]) -> None: ...
    @property
    def GET(self) -> _ImmutableQueryDict: ...  # type: ignore
    POST: _ImmutableQueryDict
    FILES: MultiValueDict
    @property
    def COOKIES(self) -> dict[str, str]: ...  # type: ignore

_T = TypeVar("_T")

class ASGIHandler(base.BaseHandler):
    request_class: type[ASGIRequest]
    chunk_size: int
    def __init__(self) -> None: ...
    async def __call__(
        self,
        scope: dict[str, Any],
        receive: _ReceiveCallback,
        send: _SendCallback,
    ) -> None: ...
    async def read_body(self, receive: _ReceiveCallback) -> IO[bytes]: ...
    def create_request(
        self, scope: Mapping[str, Any], body_file: IO[bytes]
    ) -> tuple[ASGIRequest, None] | tuple[None, HttpResponseBase]: ...
    def handle_uncaught_exception(
        self, request: HttpRequest, resolver: URLResolver, exc_info: Any
    ) -> HttpResponseBase: ...
    async def send_response(self, response: HttpResponseBase, send: _SendCallback) -> None: ...
    @classmethod
    def chunk_bytes(cls, data: Sequence[_T]) -> Iterator[tuple[Sequence[_T], bool]]: ...
    def get_script_prefix(self, scope: Mapping[str, Any]) -> str: ...
