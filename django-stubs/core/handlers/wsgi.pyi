from collections.abc import Callable, Sequence
from io import BytesIO
from typing import Any

from django.contrib.sessions.backends.base import SessionBase
from django.core.handlers import base
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from typing_extensions import TypeAlias

_WSGIEnviron: TypeAlias = dict[str, Any]

class LimitedStream:
    stream: BytesIO
    remaining: int
    buffer: bytes
    buf_size: int
    def __init__(self, stream: BytesIO, limit: int, buf_size: int = ...) -> None: ...
    def read(self, size: int | None = ...) -> bytes: ...
    def readline(self, size: int | None = ...) -> bytes: ...

class WSGIRequest(HttpRequest):
    environ: _WSGIEnviron
    session: SessionBase
    encoding: Any
    def __init__(self, environ: _WSGIEnviron) -> None: ...

class WSGIHandler(base.BaseHandler):
    request_class: type[WSGIRequest]
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __call__(
        self,
        environ: _WSGIEnviron,
        start_response: Callable[[str, Sequence[tuple[str, str]]], None],
    ) -> HttpResponseBase: ...

def get_path_info(environ: _WSGIEnviron) -> str: ...
def get_script_name(environ: _WSGIEnviron) -> str: ...
def get_bytes_from_wsgi(environ: _WSGIEnviron, key: str, default: str) -> bytes: ...
def get_str_from_wsgi(environ: _WSGIEnviron, key: str, default: str) -> str: ...
