import collections
import uuid
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Type, Union

from django.db.models.base import Model
from django.db.models.expressions import Case
from django.db.models.query import QuerySet
from django.db.models.sql.datastructures import BaseTable
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

from django.db.models.fields import Field

class DeleteQuery(Query):
    alias_refcount: Dict[str, int]
    annotation_select_mask: None
    base_table: str
    combinator: None
    combinator_all: bool
    combined_queries: Tuple
    default_cols: bool
    default_ordering: bool
    deferred_loading: Tuple[frozenset, bool]
    distinct: bool
    distinct_fields: Tuple
    explain_format: None
    explain_options: Dict[Any, Any]
    explain_query: bool
    external_aliases: Set[Any]
    extra_order_by: Tuple
    extra_select_mask: None
    extra_tables: Tuple
    filter_is_sticky: bool
    group_by: None
    high_mark: None
    low_mark: int
    max_depth: int
    model: Type[Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    subq_aliases: frozenset
    subquery: bool
    table_map: Dict[str, List[str]]
    used_aliases: Set[str]
    values_select: Tuple
    where_class: Type[WhereNode]
    compiler: str = ...
    where: WhereNode = ...
    def do_query(self, table: str, where: WhereNode, using: str) -> int: ...
    def delete_batch(self, pk_list: Union[List[int], List[str]], using: str) -> int: ...
    def delete_qs(self, query: QuerySet, using: str) -> int: ...

class UpdateQuery(Query):
    alias_refcount: Dict[str, int]
    annotation_select_mask: Optional[Set[Any]]
    base_table: str
    combinator: None
    combinator_all: bool
    combined_queries: Tuple
    default_cols: bool
    default_ordering: bool
    deferred_loading: Tuple[frozenset, bool]
    distinct: bool
    distinct_fields: Tuple
    explain_format: None
    explain_options: Dict[Any, Any]
    explain_query: bool
    external_aliases: Set[Any]
    extra_order_by: Tuple
    extra_select_mask: Optional[Set[Any]]
    extra_tables: Tuple
    filter_is_sticky: bool
    group_by: Optional[bool]
    high_mark: None
    low_mark: int
    max_depth: int
    model: Type[Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    subq_aliases: frozenset
    subquery: bool
    table_map: Dict[str, List[str]]
    used_aliases: Set[str]
    values: List[Tuple[Field, Optional[Type[Model]], Union[Case, uuid.UUID]]]
    values_select: Tuple
    where_class: Type[WhereNode]
    compiler: str = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def clone(self) -> UpdateQuery: ...
    where: WhereNode = ...
    def update_batch(self, pk_list: List[int], values: Dict[str, Optional[int]], using: str) -> None: ...
    def add_update_values(self, values: Dict[str, Any]) -> None: ...
    def add_update_fields(self, values_seq: List[Tuple[Field, Optional[Type[Model]], Case]]) -> None: ...
    def add_related_update(self, model: Type[Model], field: Field, value: Union[int, str]) -> None: ...
    def get_related_updates(self) -> List[UpdateQuery]: ...

class InsertQuery(Query):
    alias_refcount: Dict[str, int]
    annotation_select_mask: None
    combinator: None
    combinator_all: bool
    combined_queries: Tuple
    default_cols: bool
    default_ordering: bool
    deferred_loading: Tuple[frozenset, bool]
    distinct: bool
    distinct_fields: Tuple
    explain_format: None
    explain_options: Dict[Any, Any]
    explain_query: bool
    external_aliases: Set[Any]
    extra_order_by: Tuple
    extra_select_mask: None
    extra_tables: Tuple
    filter_is_sticky: bool
    group_by: None
    high_mark: None
    low_mark: int
    max_depth: int
    model: Type[Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    subquery: bool
    table_map: Dict[str, List[str]]
    used_aliases: Set[Any]
    values_select: Tuple
    where: WhereNode
    where_class: Type[WhereNode]
    compiler: str = ...
    fields: Iterable[Field] = ...
    objs: List[Model] = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    raw: bool = ...
    def insert_values(self, fields: Iterable[Field], objs: List[Model], raw: bool = ...) -> None: ...

class AggregateQuery(Query):
    alias_refcount: Dict[Any, Any]
    annotation_select_mask: None
    combinator: None
    combinator_all: bool
    combined_queries: Tuple
    default_cols: bool
    default_ordering: bool
    deferred_loading: Tuple[frozenset, bool]
    distinct: bool
    distinct_fields: Tuple
    explain_format: None
    explain_options: Dict[Any, Any]
    explain_query: bool
    external_aliases: Set[Any]
    extra_order_by: Tuple
    extra_select_mask: None
    extra_tables: Tuple
    filter_is_sticky: bool
    group_by: None
    high_mark: None
    low_mark: int
    max_depth: int
    model: Type[Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    sub_params: Tuple
    table_map: Dict[Any, Any]
    used_aliases: Set[Any]
    values_select: Tuple
    where: WhereNode
    where_class: Type[WhereNode]
    compiler: str = ...
    def add_subquery(self, query: Query, using: str) -> None: ...
