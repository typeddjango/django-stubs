from typing import Any, Awaitable, Callable, Dict, Mapping, Sequence, Tuple
from urllib.parse import ParseResult

from django.core.handlers.asgi import ASGIHandler, ASGIRequest
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIHandler, WSGIRequest
from django.http import HttpRequest
from django.http.response import HttpResponseBase

class StaticFilesHandlerMixin:
    handles_files: bool = ...
    application: BaseHandler
    base_url: ParseResult
    def load_middleware(self) -> None: ...
    def get_base_url(self) -> str: ...
    def _should_handle(self, path: str) -> bool: ...
    def file_path(self, url: str) -> str: ...
    def serve(self, request: HttpRequest) -> HttpResponseBase: ...
    def get_response(self, request: HttpRequest) -> HttpResponseBase: ...
    async def get_response_async(self, request: HttpRequest) -> HttpResponseBase: ...

class StaticFilesHandler(StaticFilesHandlerMixin, WSGIHandler):  # type: ignore
    application: WSGIHandler
    base_url: ParseResult
    def __init__(self, application: WSGIHandler) -> None: ...
    def __call__(
        self,
        environ: Dict[str, Any],
        start_response: Callable[[str, Sequence[Tuple[str, str]]], None],
    ) -> HttpResponseBase: ...

class ASGIStaticFilesHandler(StaticFilesHandlerMixin, ASGIHandler):  # type: ignore
    application: ASGIHandler
    base_url: ParseResult
    def __init__(self, application: ASGIHandler) -> None: ...
    async def __call__(
        self,
        scope: Dict[str, Any],
        receive: Callable[[], Awaitable[Mapping[str, Any]]],
        send: Callable[[Mapping[str, Any]], Awaitable[None]],
    ) -> None: ...
