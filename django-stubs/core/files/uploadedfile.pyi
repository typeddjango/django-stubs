from io import (
    BytesIO,
    StringIO,
)
from tempfile import _TemporaryFileWrapper
from typing import (
    Iterator,
    Optional,
    Union,
)


class InMemoryUploadedFile:
    def __init__(
        self,
        file: Union[StringIO, BytesIO],
        field_name: Optional[str],
        name: str,
        content_type: str,
        size: int,
        charset: Optional[str],
        content_type_extra: None = ...
    ) -> None: ...
    def chunks(self, chunk_size: None = ...) -> Iterator[Union[str, bytes]]: ...
    def open(self, mode: None = ...) -> InMemoryUploadedFile: ...


class SimpleUploadedFile:
    def __init__(self, name: str, content: Optional[bytes], content_type: str = ...) -> None: ...


class TemporaryUploadedFile:
    def __init__(
        self,
        name: str,
        content_type: str,
        size: int,
        charset: str,
        content_type_extra: None = ...
    ) -> None: ...
    def close(self) -> None: ...
    def temporary_file_path(self) -> str: ...


class UploadedFile:
    def __init__(
        self,
        file: Optional[Union[StringIO, _TemporaryFileWrapper, BytesIO]] = ...,
        name: str = ...,
        content_type: str = ...,
        size: Optional[int] = ...,
        charset: Optional[str] = ...,
        content_type_extra: None = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    def _get_name(self) -> str: ...
    def _set_name(self, name: str) -> None: ...