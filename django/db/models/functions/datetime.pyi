from datetime import (
    date,
    time,
)
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import Col
from django.db.models.fields import (
    DateTimeCheckMixin,
    IntegerField,
)
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Union,
)


class Extract:
    def __init__(
        self,
        expression: Union[str, Col, TruncDate],
        lookup_name: Optional[str] = ...,
        tzinfo: None = ...,
        **extra
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: None = ...,
        summarize: bool = ...,
        for_save: bool = ...
    ) -> Extract: ...


class TimezoneMixin:
    def get_tzname(self) -> Optional[str]: ...


class Trunc:
    def __init__(
        self,
        expression: str,
        kind: str,
        output_field: Optional[Union[IntegerField, DateTimeCheckMixin]] = ...,
        tzinfo: None = ...,
        **extra
    ) -> None: ...


class TruncBase:
    def __init__(
        self,
        expression: Union[str, Col],
        output_field: Optional[DateTimeCheckMixin] = ...,
        tzinfo: None = ...,
        **extra
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...
    def convert_value(
        self,
        value: Union[date, time],
        expression: django.db.models.functions.TruncBase,
        connection: DatabaseWrapper
    ) -> Union[date, time]: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: None = ...,
        summarize: bool = ...,
        for_save: bool = ...
    ) -> TruncBase: ...


class TruncDate:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...


class TruncTime:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...