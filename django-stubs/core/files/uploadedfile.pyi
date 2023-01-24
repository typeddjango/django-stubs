from typing import IO, AnyStr, TypeVar

from _typeshed import Self
from django.core.files.base import File

class UploadedFile(File[AnyStr]):
    content_type: str | None
    charset: str | None
    content_type_extra: dict[str, str] | None
    size: int | None  # type: ignore[assignment]
    name: str | None
    def __init__(
        self,
        file: IO[AnyStr] | None = ...,
        name: str | None = ...,
        content_type: str | None = ...,
        size: int | None = ...,
        charset: str | None = ...,
        content_type_extra: dict[str, str] | None = ...,
    ) -> None: ...

class TemporaryUploadedFile(UploadedFile[AnyStr]):
    def __init__(
        self,
        name: str,
        content_type: str | None,
        size: int | None,
        charset: str | None,
        content_type_extra: dict[str, str] | None = ...,
    ) -> None: ...
    def temporary_file_path(self) -> str: ...

class InMemoryUploadedFile(UploadedFile[AnyStr]):
    field_name: str | None
    def __init__(
        self,
        file: IO[AnyStr],
        field_name: str | None,
        name: str | None,
        content_type: str | None,
        size: int | None,
        charset: str | None,
        content_type_extra: dict[str, str] = ...,
    ) -> None: ...

class SimpleUploadedFile(InMemoryUploadedFile[AnyStr]):
    def __init__(self, name: str, content: bytes | None, content_type: str = ...) -> None: ...
    @classmethod
    def from_dict(cls: type[Self], file_dict: dict[str, str | bytes]) -> Self: ...
