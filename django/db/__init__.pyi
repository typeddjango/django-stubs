from django.db.backends.sqlite3.base import DatabaseWrapper
from typing import (
    Any,
    Union,
)
from unittest.mock import MagicMock


def close_old_connections(**kwargs) -> None: ...


def reset_queries(**kwargs) -> None: ...


class DefaultConnectionProxy:
    def __eq__(self, other: DatabaseWrapper) -> bool: ...
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, name: str, value: Union[MagicMock, bool]) -> None: ...