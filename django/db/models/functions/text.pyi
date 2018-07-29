from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import (
    Col,
    F,
    Value,
)
from django.db.models.sql.compiler import SQLCompiler
from typing import (
    Any,
    List,
    Tuple,
    Union,
)


class BytesToCharFieldConversionMixin:
    def convert_value(
        self,
        value: str,
        expression: LPad,
        connection: DatabaseWrapper
    ) -> str: ...


class Chr:
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[Any]]]: ...


class Concat:
    def __init__(self, *expressions, **extra) -> None: ...
    def _paired(
        self,
        expressions: Union[Tuple[Value, str], Tuple[str, str], Tuple[Value, str, Value]]
    ) -> ConcatPair: ...


class ConcatPair:
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...
    def coalesce(self) -> ConcatPair: ...


class LPad:
    def __init__(
        self,
        expression: str,
        length: Union[int, Length],
        fill_text: Value = ...,
        **extra
    ) -> None: ...


class Left:
    def __init__(self, expression: str, length: int, **extra) -> None: ...
    def get_substr(self) -> Substr: ...
    def use_substr(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context
    ) -> Tuple[str, List[int]]: ...


class Ord:
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context
    ) -> Union[Tuple[str, List[Any]], Tuple[str, List[str]]]: ...


class Replace:
    def __init__(
        self,
        expression: F,
        text: Value,
        replacement: Value = ...,
        **extra
    ) -> None: ...


class Right:
    def get_substr(self) -> Substr: ...


class Substr:
    def __init__(
        self,
        expression: Union[str, Col],
        pos: Union[int, Value],
        length: Union[int, Value] = ...,
        **extra
    ) -> None: ...
    def as_oracle(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[int]]: ...
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[Union[str, int]]]]: ...