from io import BytesIO
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from django.core.handlers.wsgi import WSGIRequest
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)


def load_handler(path: str, *args, **kwargs) -> FileUploadHandler: ...


class FileUploadHandler:
    def __init__(self, request: WSGIRequest = ...) -> None: ...
    def handle_raw_input(
        self,
        input_data: WSGIRequest,
        META: Dict[str, Any],
        content_length: int,
        boundary: bytes,
        encoding: str = ...
    ) -> None: ...
    def new_file(
        self,
        field_name: str,
        file_name: str,
        content_type: str,
        content_length: None,
        charset: None = ...,
        content_type_extra: Dict[Any, Any] = ...
    ) -> None: ...
    def upload_complete(self) -> None: ...


class MemoryFileUploadHandler:
    def file_complete(self, file_size: int) -> Optional[InMemoryUploadedFile]: ...
    def handle_raw_input(
        self,
        input_data: Union[BytesIO, WSGIRequest],
        META: Dict[str, Any],
        content_length: int,
        boundary: bytes,
        encoding: str = ...
    ) -> None: ...
    def new_file(self, *args, **kwargs) -> None: ...
    def receive_data_chunk(self, raw_data: bytes, start: int) -> Optional[bytes]: ...


class TemporaryFileUploadHandler:
    def file_complete(self, file_size: int) -> TemporaryUploadedFile: ...
    def new_file(self, *args, **kwargs) -> None: ...
    def receive_data_chunk(self, raw_data: bytes, start: int) -> None: ...