from typing import Any, Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import FileResponse

def serve(request: WSGIRequest, path: str, document_root: str = ..., show_indexes: bool = ...) -> FileResponse: ...

DEFAULT_DIRECTORY_INDEX_TEMPLATE: str
template_translatable: Any

def directory_index(path: Any, fullpath: Any): ...
def was_modified_since(header: None = ..., mtime: float = ..., size: int = ...) -> bool: ...
