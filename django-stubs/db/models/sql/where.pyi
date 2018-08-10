from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Union

from django.db import DefaultConnectionProxy
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import Expression
from django.db.models.lookups import FieldGetDbPrepValueMixin
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.utils import tree

AND: str
OR: str

class WhereNode(tree.Node):
    connector: str
    contains_aggregate: bool
    contains_over_clause: bool
    negated: bool
    default: Any = ...
    resolved: bool = ...
    conditional: bool = ...
    def split_having(
        self, negated: bool = ...
    ) -> Tuple[Optional[WhereNode], Optional[WhereNode]]: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: Union[DefaultConnectionProxy, DatabaseWrapper],
    ) -> Tuple[
        str,
        Union[
            List[Optional[int]],
            List[Union[date, str]],
            List[Union[Decimal, int]],
            List[Union[float, int]],
            List[Union[int, str]],
            List[memoryview],
        ],
    ]: ...
    def get_group_by_cols(self) -> List[Expression]: ...
    def get_source_expressions(self) -> List[FieldGetDbPrepValueMixin]: ...
    children: Union[
        List[
            Union[
                django.db.models.lookups.BuiltinLookup,
                django.db.models.sql.where.ExtraWhere,
            ]
        ],
        List[
            Union[
                django.db.models.lookups.FieldGetDbPrepValueMixin,
                django.db.models.lookups.Lookup,
                django.db.models.sql.where.NothingNode,
                django.db.models.sql.where.WhereNode,
            ]
        ],
        List[
            Union[
                django.db.models.lookups.FieldGetDbPrepValueMixin,
                django.db.models.query_utils.QueryWrapper,
            ]
        ],
        List[
            Union[
                django.db.models.sql.where.SubqueryConstraint,
                django.db.models.sql.where.WhereNode,
            ]
        ],
    ] = ...
    def set_source_expressions(
        self, children: List[FieldGetDbPrepValueMixin]
    ) -> None: ...
    def relabel_aliases(self, change_map: Dict[Optional[str], str]) -> None: ...
    def clone(self) -> WhereNode: ...
    def relabeled_clone(
        self, change_map: Dict[Optional[str], str]
    ) -> WhereNode: ...
    def contains_aggregate(self) -> bool: ...
    def contains_over_clause(self) -> bool: ...
    @property
    def is_summary(self): ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> WhereNode: ...

class NothingNode:
    contains_aggregate: bool = ...
    def as_sql(
        self,
        compiler: SQLCompiler = ...,
        connection: Union[DefaultConnectionProxy, DatabaseWrapper] = ...,
    ) -> Any: ...

class ExtraWhere:
    contains_aggregate: bool = ...
    sqls: List[str] = ...
    params: Optional[Union[List[int], List[str]]] = ...
    def __init__(
        self, sqls: List[str], params: Optional[Union[List[int], List[str]]]
    ) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler = ..., connection: DatabaseWrapper = ...
    ) -> Tuple[str, Union[List[int], List[str]]]: ...

class SubqueryConstraint:
    contains_aggregate: bool = ...
    alias: str = ...
    columns: List[str] = ...
    targets: List[str] = ...
    query_object: django.db.models.sql.query.Query = ...
    def __init__(
        self,
        alias: str,
        columns: List[str],
        targets: List[str],
        query_object: Query,
    ) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, Tuple]: ...
