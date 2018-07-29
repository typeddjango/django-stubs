from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.fields import Field
from django.db.models.query_utils import Q
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


class Aggregate:
    def __init__(self, *args, filter = ..., **kwargs) -> None: ...
    def _get_repr_options(self) -> Dict[str, Q]: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        **extra_context
    ) -> Any: ...
    @property
    def default_alias(self) -> str: ...
    def get_group_by_cols(self) -> List[Any]: ...
    def get_source_expressions(self) -> Any: ...
    def get_source_fields(self) -> Any: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: None = ...,
        summarize: bool = ...,
        for_save: bool = ...
    ) -> Aggregate: ...
    def set_source_expressions(self, exprs: Any) -> None: ...


class Avg:
    def _resolve_output_field(self) -> Field: ...


class Count:
    def __init__(
        self,
        expression: str,
        distinct: bool = ...,
        filter: Optional[Q] = ...,
        **extra
    ) -> None: ...
    def _get_repr_options(self) -> Dict[str, bool]: ...
    def convert_value(
        self,
        value: Optional[int],
        expression: Count,
        connection: DatabaseWrapper
    ) -> int: ...


class StdDev:
    def __init__(self, expression: str, sample: bool = ..., **extra) -> None: ...


class Variance:
    def __init__(self, expression: str, sample: bool = ..., **extra) -> None: ...
    def _get_repr_options(self) -> Dict[str, bool]: ...