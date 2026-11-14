from collections.abc import Mapping
from re import Pattern
from typing import Any

from django.utils.functional import SimpleLazyObject

class ExternalCRSBlocker:
    AUTHORITIES: frozenset[str]
    AUTHORITY_CODE: SimpleLazyObject[Pattern[str]]
    OGC_URN: SimpleLazyObject[Pattern[str]]
    BARE: frozenset[str]

    @classmethod
    def check(cls, value: str) -> None: ...
    @staticmethod
    def normalize_key(key: str) -> str: ...
    @classmethod
    def check_member(cls, member: Mapping[str, Any]) -> None: ...
    @classmethod
    def check_crs_name(cls, name: str) -> None: ...
