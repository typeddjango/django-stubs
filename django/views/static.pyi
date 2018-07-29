from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    FileResponse,
    HttpResponse,
)
from pathlib import PosixPath
from typing import (
    Optional,
    Union,
)


def directory_index(path: str, fullpath: PosixPath) -> HttpResponse: ...


def serve(
    request: WSGIRequest,
    path: str,
    document_root: str = ...,
    show_indexes: bool = ...
) -> Union[HttpResponse, FileResponse]: ...


def was_modified_since(header: Optional[str] = ..., mtime: float = ..., size: int = ...) -> bool: ...