from datetime import date, time, timedelta
from decimal import Decimal
from typing import Any, Dict, Optional, Union
from uuid import UUID

from django.db.models.base import Model
from django.db.models.fields.files import FieldFile


class DjangoUnicodeDecodeError(UnicodeDecodeError):
    obj: bytes = ...
    def __init__(self, obj: bytes, *args: Any) -> None: ...

python_2_unicode_compatible: Any

def smart_text(
    s: Union[Model, int, str],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> str: ...
def is_protected_type(
    obj: Optional[
        Union[
            date,
            time,
            timedelta,
            Decimal,
            FieldFile,
            float,
            int,
            memoryview,
            str,
            UUID,
        ]
    ]
) -> bool: ...
def force_text(
    s: Optional[Union[bytes, Model, int, str]],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> Optional[Union[int, str]]: ...
def smart_bytes(
    s: Union[int, str],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> bytes: ...
def force_bytes(
    s: Union[
        Dict[str, str], ValueError, bytes, date, int, memoryview, str, UUID
    ],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> Union[bytes, date]: ...

smart_str = smart_text
force_str = force_text

def iri_to_uri(iri: Optional[str]) -> Optional[str]: ...
def uri_to_iri(uri: Optional[str]) -> Optional[str]: ...
def escape_uri_path(path: str) -> str: ...
def repercent_broken_unicode(path: bytes) -> bytes: ...
def filepath_to_uri(path: Optional[str]) -> Optional[str]: ...
def get_system_encoding() -> str: ...

DEFAULT_LOCALE_ENCODING: Any
