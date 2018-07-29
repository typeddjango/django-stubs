from datetime import date
from django.db.models.base import Model
from typing import (
    Any,
    Optional,
    Union,
)


def escape_uri_path(path: str) -> str: ...


def filepath_to_uri(path: Optional[str]) -> Optional[str]: ...


def force_bytes(
    s: Any,
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...
) -> Union[date, bytes]: ...


def force_text(s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...) -> Optional[str]: ...


def get_system_encoding() -> str: ...


def iri_to_uri(iri: Optional[str]) -> Optional[str]: ...


def is_protected_type(obj: Any) -> bool: ...


def repercent_broken_unicode(path: bytes) -> bytes: ...


def smart_text(
    s: Union[Model, int, str],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...
) -> str: ...


def uri_to_iri(uri: Optional[str]) -> Optional[str]: ...


class DjangoUnicodeDecodeError:
    def __init__(self, obj: bytes, *args) -> None: ...
    def __str__(self) -> str: ...