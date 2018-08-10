from datetime import date, datetime
from decimal import Decimal
from typing import Any, List, Optional, Tuple, Union

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models import Func
from django.db.models.expressions import Value
from django.db.models.fields import Field
from django.db.models.sql.compiler import SQLCompiler


class Cast(Func):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.Field
    source_expressions: List[django.db.models.expressions.Combinable]
    function: str = ...
    template: str = ...
    def __init__(
        self, expression: Union[date, Decimal, Value, str], output_field: Field
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context: Any
    ) -> Tuple[str, Union[List[date], List[Decimal], List[str]]]: ...
    def as_mysql(self, compiler: Any, connection: Any): ...
    def as_postgresql(self, compiler: Any, connection: Any): ...

class Coalesce(Func):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.Field
    source_expressions: List[django.db.models.expressions.Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...
    def as_oracle(self, compiler: Any, connection: Any): ...

class Greatest(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.Field
    source_expressions: List[django.db.models.expressions.Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...
    def as_sqlite(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[datetime]]: ...

class Least(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: django.db.models.fields.Field
    source_expressions: List[django.db.models.expressions.Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...
    def as_sqlite(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[datetime]]: ...
