from datetime import (
    date,
    time,
)
from decimal import Decimal
from django.db.backends.sqlite3.base import (
    DatabaseWrapper,
    SQLiteCursorWrapper,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def format_number(
    value: Optional[Decimal],
    max_digits: Optional[int],
    decimal_places: Optional[int]
) -> Optional[str]: ...


def rev_typecast_decimal(d: Decimal) -> str: ...


def split_identifier(identifier: str) -> Tuple[str, str]: ...


def strip_quotes(table_name: str) -> str: ...


def truncate_name(identifier: str, length: Optional[int] = ..., hash_len: int = ...) -> str: ...


def typecast_date(s: str) -> date: ...


def typecast_time(s: str) -> Optional[time]: ...


def typecast_timestamp(s: str) -> date: ...


class CursorDebugWrapper:
    def execute(self, sql: str, params: Optional[Union[List[str], Tuple]] = ...): ...


class CursorWrapper:
    def __enter__(self) -> CursorWrapper: ...
    def __exit__(self, type: None, value: None, traceback: None) -> None: ...
    def __getattr__(self, attr: str) -> Any: ...
    def __init__(
        self,
        cursor: SQLiteCursorWrapper,
        db: DatabaseWrapper
    ) -> None: ...
    def __iter__(self) -> None: ...
    def _execute(self, sql: str, params: Any, *ignored_wrapper_args): ...
    def _execute_with_wrappers(
        self,
        sql: str,
        params: Any,
        many: bool,
        executor: Callable
    ) -> Optional[SQLiteCursorWrapper]: ...
    def _executemany(
        self,
        sql: str,
        param_list: Union[List[Tuple[int]], List[Tuple[int, int, int]]],
        *ignored_wrapper_args
    ): ...
    def callproc(self, procname: str, params: List[Any] = ..., kparams: Dict[str, int] = ...): ...
    def execute(self, sql: str, params: Any = ...) -> SQLiteCursorWrapper: ...