from typing import Any, Optional

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase

def serve(
    request: HttpRequest, path: str, document_root: Optional[str] = ..., show_indexes: bool = ...
) -> HttpResponseBase: ...

DEFAULT_DIRECTORY_INDEX_TEMPLATE: str
template_translatable: Any

def directory_index(path: Any, fullpath: Any): ...
def was_modified_since(header: Optional[str] = ..., mtime: float = ..., size: int = ...) -> bool: ...
