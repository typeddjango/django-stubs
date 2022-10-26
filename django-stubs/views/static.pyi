from typing import Any, Optional

from django.http import FileResponse, HttpResponse
from django.http.request import HttpRequest

def serve(
    request: HttpRequest, path: str, document_root: Optional[str] = ..., show_indexes: bool = ...
) -> FileResponse: ...

DEFAULT_DIRECTORY_INDEX_TEMPLATE: str
template_translatable: Any

def directory_index(path: Any, fullpath: Any) -> HttpResponse: ...
def was_modified_since(header: Optional[str] = ..., mtime: float = ..., size: int = ...) -> bool: ...
