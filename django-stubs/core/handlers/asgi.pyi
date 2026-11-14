from collections.abc import Iterator, Mapping, Sequence
from logging import Logger
from typing import IO, Any

from _typeshed import ExcInfo
from asgiref.typing import ASGIReceiveCallable, ASGISendCallable, Scope
from django.core.files import uploadedfile
from django.core.handlers import base
from django.http.request import HttpRequest, _ImmutableQueryDict
from django.http.response import HttpResponseBase
from django.urls.resolvers import ResolverMatch, URLResolver
from django.utils.datastructures import MultiValueDict
from django.utils.functional import cached_property
from typing_extensions import TypeVar, override

logger: Logger

def get_script_prefix(scope: Mapping[str, Any]) -> str: ...

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
    @cached_property
    @override
    def GET(self) -> _ImmutableQueryDict: ...  # type: ignore[override]
    POST: _ImmutableQueryDict
    @property
    @override
    def FILES(self) -> MultiValueDict[str, uploadedfile.UploadedFile[Any]]: ...  # type: ignore[override]
    @cached_property
    @override
    def COOKIES(self) -> dict[str, str]: ...  # type: ignore[override]

_T = TypeVar("_T")

class ASGIHandler(base.BaseHandler):
    request_class: type[ASGIRequest]
    chunk_size: int
    def __init__(self) -> None: ...
    async def __call__(
        self,
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...
    async def handle(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> HttpResponseBase | None: ...
    async def listen_for_disconnect(self, receive: ASGIReceiveCallable) -> None: ...
    async def run_get_response(self, request: HttpRequest) -> HttpResponseBase: ...
    async def read_body(self, receive: ASGIReceiveCallable) -> IO[bytes]: ...
    def create_request(
        self, scope: Mapping[str, Any], body_file: IO[bytes]
    ) -> tuple[ASGIRequest, None] | tuple[None, HttpResponseBase]: ...
    def handle_uncaught_exception(
        self, request: HttpRequest, resolver: URLResolver, exc_info: ExcInfo
    ) -> HttpResponseBase: ...
    async def send_response(self, response: HttpResponseBase, send: ASGISendCallable) -> None: ...
    @classmethod
    def chunk_bytes(cls, data: Sequence[_T]) -> Iterator[tuple[Sequence[_T], bool]]: ...
