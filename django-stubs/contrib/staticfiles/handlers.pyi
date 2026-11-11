from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias
from urllib.parse import ParseResult
from wsgiref.types import StartResponse, WSGIEnvironment

from django.core.handlers.asgi import ASGIHandler, _ReceiveCallback, _SendCallback
from django.core.handlers.wsgi import WSGIHandler
from django.http import HttpRequest
from django.http.response import FileResponse, HttpResponse, HttpResponseBase
from typing_extensions import override

_ASGIApplication: TypeAlias = Callable[[dict[str, Any], _ReceiveCallback, _SendCallback], Awaitable[None]]

class StaticFilesHandlerMixin:
    handles_files: bool
    base_url: ParseResult
    def load_middleware(self) -> None: ...
    def get_base_url(self) -> str: ...
    def _should_handle(self, path: str) -> bool: ...
    def file_path(self, url: str) -> str: ...
    def serve(self, request: HttpRequest) -> HttpResponse | FileResponse: ...
    def get_response(self, request: HttpRequest) -> HttpResponseBase: ...
    async def get_response_async(self, request: HttpRequest) -> HttpResponseBase: ...

class StaticFilesHandler(StaticFilesHandlerMixin, WSGIHandler):  # type: ignore[misc]
    application: WSGIHandler
    base_url: ParseResult
    def __init__(self, application: WSGIHandler) -> None: ...
    @override
    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: StartResponse,
    ) -> HttpResponseBase: ...

class ASGIStaticFilesHandler(StaticFilesHandlerMixin, ASGIHandler):  # type: ignore[misc]
    application: _ASGIApplication
    base_url: ParseResult
    def __init__(self, application: _ASGIApplication) -> None: ...
    @override
    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[Mapping[str, Any]]],
        send: Callable[[Mapping[str, Any]], Awaitable[None]],
    ) -> None: ...
