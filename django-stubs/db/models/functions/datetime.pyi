from datetime import date, time
from typing import Any, List, Optional, Set, Tuple, Union

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models import Func, Transform
from django.db.models.expressions import Col, Expression
from django.db.models.fields import Field
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query


class TimezoneMixin:
    tzinfo: Any = ...
    def get_tzname(self) -> Optional[str]: ...

class Extract(TimezoneMixin, Transform):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    lookup_name: Optional[str] = ...
    output_field: Any = ...
    tzinfo: None = ...
    def __init__(
        self,
        expression: Union[Expression, str],
        lookup_name: Optional[str] = ...,
        tzinfo: None = ...,
        **extra: Any
    ) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: Optional[Set[Any]] = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> Extract: ...

class ExtractYear(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractMonth(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractDay(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractWeek(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractWeekDay(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractQuarter(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractHour(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractMinute(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class ExtractSecond(Extract):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    lookup_name: str = ...

class Now(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[Any]
    template: str = ...
    output_field: Any = ...
    def as_postgresql(self, compiler: Any, connection: Any): ...

class TruncBase(TimezoneMixin, Transform):
    kind: Any = ...
    tzinfo: Any = ...
    def __init__(
        self,
        expression: Union[Col, str],
        output_field: Optional[Field] = ...,
        tzinfo: None = ...,
        **extra: Any
    ) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: Optional[Set[Any]] = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> TruncBase: ...
    def convert_value(
        self,
        value: Union[date, time],
        expression: django.db.models.functions.TruncBase,
        connection: DatabaseWrapper,
    ) -> Union[date, time]: ...

class Trunc(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: Union[
        django.db.models.fields.DateTimeCheckMixin,
        django.db.models.fields.IntegerField,
    ]
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...
    def __init__(
        self,
        expression: str,
        kind: str,
        output_field: Optional[Field] = ...,
        tzinfo: None = ...,
        **extra: Any
    ) -> None: ...

class TruncYear(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncQuarter(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncMonth(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncWeek(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncDay(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncDate(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...
    lookup_name: str = ...
    output_field: django.db.models.fields.TimeField = ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...

class TruncTime(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...
    lookup_name: str = ...
    output_field: django.db.models.fields.DateField = ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...

class TruncHour(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncMinute(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...

class TruncSecond(TruncBase):
    contains_aggregate: bool
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.DateTimeCheckMixin
    source_expressions: List[django.db.models.expressions.Combinable]
    tzinfo: None
    kind: str = ...
