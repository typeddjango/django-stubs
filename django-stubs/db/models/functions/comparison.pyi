from datetime import (
    date,
    datetime,
)
from decimal import Decimal
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.fields import Field
from django.db.models.sql.compiler import SQLCompiler
from typing import (
    Any,
    List,
    Tuple,
    Union,
)


class Cast:
    def __init__(
        self,
        expression: Union[str, date, Decimal],
        output_field: Field
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context
    ) -> Union[Tuple[str, List[datetime]], Tuple[str, List[Any]]]: ...


class Coalesce:
    def __init__(self, *expressions, **extra) -> None: ...


class Greatest:
    def __init__(self, *expressions, **extra) -> None: ...
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...


class Least:
    def __init__(self, *expressions, **extra) -> None: ...
    def as_sqlite(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[datetime]], Tuple[str, List[Any]]]: ...