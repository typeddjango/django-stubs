import datetime
import sys
import types
from contextlib import contextmanager
from decimal import Decimal
from typing import Any, Dict, Generator, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, Union, overload
from uuid import UUID

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

logger: Any

# Python types that can be adapted to SQL.
_SQLType = Union[
    None, bool, int, float, Decimal, str, bytes, datetime.date, datetime.datetime, UUID, Tuple[Any, ...], List[Any]
]
_ExecuteParameters = Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]]

class CursorWrapper:
    cursor: Any = ...
    db: Any = ...
    def __init__(self, cursor: Any, db: Any) -> None: ...
    WRAP_ERROR_ATTRS: Any = ...
    def __getattr__(self, attr: str) -> Any: ...
    def __iter__(self) -> Iterator[Tuple[Any, ...]]: ...
    def __enter__(self) -> CursorWrapper: ...
    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> None: ...
    def callproc(
        self, procname: str, params: Optional[Sequence[Any]] = ..., kparams: Optional[Dict[str, int]] = ...
    ) -> Any: ...
    def execute(self, sql: str, params: _ExecuteParameters = ...) -> Any: ...
    def executemany(self, sql: str, param_list: Sequence[_ExecuteParameters]) -> Any: ...

class CursorDebugWrapper(CursorWrapper):
    cursor: Any
    db: Any
    @contextmanager
    def debug_sql(
        self,
        sql: Optional[str] = ...,
        params: Optional[Union[_ExecuteParameters, Sequence[_ExecuteParameters]]] = ...,
        use_last_executed_query: bool = ...,
        many: bool = ...,
    ) -> Generator[None, None, None]: ...

@overload
def typecast_date(s: Union[None, Literal[""]]) -> None: ...  # type: ignore
@overload
def typecast_date(s: str) -> datetime.date: ...
@overload
def typecast_time(s: Union[None, Literal[""]]) -> None: ...  # type: ignore
@overload
def typecast_time(s: str) -> datetime.time: ...
@overload
def typecast_timestamp(s: Union[None, Literal[""]]) -> None: ...  # type: ignore
@overload
def typecast_timestamp(s: str) -> datetime.datetime: ...
def split_identifier(identifier: str) -> Tuple[str, str]: ...
def truncate_name(identifier: str, length: Optional[int] = ..., hash_len: int = ...) -> str: ...
def format_number(
    value: Optional[Decimal], max_digits: Optional[int], decimal_places: Optional[int]
) -> Optional[str]: ...
def strip_quotes(table_name: str) -> str: ...
