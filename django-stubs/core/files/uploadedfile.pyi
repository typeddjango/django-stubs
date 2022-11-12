from typing import IO, Dict, Type, TypeVar

from django.core.files.base import File

class UploadedFile(File):
    content_type: str | None
    charset: str | None
    content_type_extra: Dict[str, str] | None
    size: int | None  # type: ignore[assignment]
    name: str | None
    def __init__(
        self,
        file: IO | None = ...,
        name: str | None = ...,
        content_type: str | None = ...,
        size: int | None = ...,
        charset: str | None = ...,
        content_type_extra: Dict[str, str] | None = ...,
    ) -> None: ...

class TemporaryUploadedFile(UploadedFile):
    def __init__(
        self,
        name: str,
        content_type: str | None,
        size: int | None,
        charset: str | None,
        content_type_extra: Dict[str, str] | None = ...,
    ) -> None: ...
    def temporary_file_path(self) -> str: ...

class InMemoryUploadedFile(UploadedFile):
    field_name: str | None
    def __init__(
        self,
        file: IO,
        field_name: str | None,
        name: str | None,
        content_type: str | None,
        size: int | None,
        charset: str | None,
        content_type_extra: Dict[str, str] = ...,
    ) -> None: ...

_C = TypeVar("_C", bound="SimpleUploadedFile")

class SimpleUploadedFile(InMemoryUploadedFile):
    def __init__(self, name: str, content: bytes | None, content_type: str = ...) -> None: ...
    @classmethod
    def from_dict(cls: Type[_C], file_dict: Dict[str, str | bytes]) -> _C: ...
