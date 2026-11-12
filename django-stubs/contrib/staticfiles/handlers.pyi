from urllib.parse import ParseResult
from wsgiref.types import StartResponse, WSGIEnvironment

from asgiref.typing import ASGI3Application, ASGIReceiveCallable, ASGISendCallable, Scope
from django.core.handlers.asgi import ASGIHandler
from django.core.handlers.wsgi import WSGIHandler
from django.http import HttpRequest
from django.http.response import FileResponse, HttpResponse, HttpResponseBase
from typing_extensions import override

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
    application: ASGI3Application
    base_url: ParseResult
    def __init__(self, application: ASGI3Application) -> None: ...
    @override
    async def __call__(
        self,
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...
