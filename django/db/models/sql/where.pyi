from collections import OrderedDict
from django.db import DefaultConnectionProxy
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import (
    Col,
    CombinedExpression,
)
from django.db.models.lookups import (
    Exact,
    FieldGetDbPrepValueMixin,
    GreaterThan,
    IntegerLessThan,
    LessThanOrEqual,
)
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class ExtraWhere:
    def __init__(self, sqls: List[str], params: Optional[List[int]]) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler = ...,
        connection: DatabaseWrapper = ...
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[Any]]]: ...


class NothingNode:
    def as_sql(
        self,
        compiler: object = ...,
        connection: Union[DefaultConnectionProxy, backends.sqlite3.base.DatabaseWrapper] = ...
    ): ...


class SubqueryConstraint:
    def __init__(
        self,
        alias: str,
        columns: List[str],
        targets: List[str],
        query_object: Query
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, Tuple]: ...


class WhereNode:
    @classmethod
    def _contains_aggregate(cls, obj: Any) -> bool: ...
    @classmethod
    def _contains_over_clause(
        cls,
        obj: Union[WhereNode, FieldGetDbPrepValueMixin]
    ) -> bool: ...
    def as_sql(
        self,
        compiler: object,
        connection: Union[DefaultConnectionProxy, backends.sqlite3.base.DatabaseWrapper]
    ) -> Any: ...
    def clone(self) -> WhereNode: ...
    @cached_property
    def contains_aggregate(self) -> bool: ...
    @cached_property
    def contains_over_clause(self) -> bool: ...
    def get_group_by_cols(
        self
    ) -> Union[List[CombinedExpression], List[Col]]: ...
    def get_source_expressions(
        self
    ) -> Union[List[GreaterThan], List[LessThanOrEqual], List[Exact], List[IntegerLessThan]]: ...
    def relabel_aliases(
        self,
        change_map: Union[OrderedDict, Dict[str, str], Dict[Union[str, None], str]]
    ) -> None: ...
    def relabeled_clone(
        self,
        change_map: Union[OrderedDict, Dict[Union[str, None], str]]
    ) -> WhereNode: ...
    def resolve_expression(self, *args, **kwargs) -> WhereNode: ...
    def set_source_expressions(
        self,
        children: Union[List[GreaterThan], List[IntegerLessThan], List[Exact]]
    ) -> None: ...
    def split_having(
        self,
        negated: bool = ...
    ) -> Union[Tuple[None, WhereNode], Tuple[WhereNode, WhereNode], Tuple[WhereNode, None]]: ...