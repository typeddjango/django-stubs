from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from django.db.models.base import Model
from django.db.models.expressions import Func
from django.db.models.fields import Field
from django.db.models.query import QuerySet
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.utils.datastructures import ImmutableList


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
    model: Type[django.db.models.base.Model]
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
    where_class: Type[django.db.models.sql.where.WhereNode]
    compiler: str = ...
    alias_map: Union[
        collections.OrderedDict,
        Dict[str, django.db.models.sql.datastructures.BaseTable],
    ] = ...
    where: django.db.models.sql.where.WhereNode = ...
    def do_query(self, table: str, where: WhereNode, using: str) -> int: ...
    def delete_batch(
        self, pk_list: Union[List[int], List[str]], using: str
    ) -> int: ...
    def delete_qs(self, query: QuerySet, using: str) -> int: ...

class UpdateQuery(Query):
    alias_map: collections.OrderedDict
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
    group_by: Optional[bool]
    high_mark: None
    low_mark: int
    max_depth: int
    model: Type[django.db.models.base.Model]
    order_by: Tuple
    related_ids: None
    related_updates: Dict[Any, Any]
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
    values: Union[
        List[
            Tuple[
                django.db.models.fields.Field,
                None,
                Union[str, datetime.date, int, None],
            ]
        ],
        List[
            Tuple[
                django.db.models.fields.related.ForeignKey,
                Type[django.db.models.base.Model],
                django.db.models.base.Model,
            ]
        ],
        List[
            Tuple[
                django.db.models.fields.related.ForeignKey,
                Type[django.db.models.base.Model],
                None,
            ]
        ],
        List[
            Tuple[
                django.db.models.fields.CharField,
                Type[django.db.models.base.Model],
                str,
            ]
        ],
    ]
    values_select: Tuple
    where_class: Type[django.db.models.sql.where.WhereNode]
    compiler: str = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def clone(self): ...
    where: django.db.models.sql.where.WhereNode = ...
    def update_batch(self, pk_list: Any, values: Any, using: Any) -> None: ...
    def add_update_values(
        self, values: Dict[str, Union[Model, Func, UUID, datetime]]
    ) -> None: ...
    def add_update_fields(self, values_seq: List) -> None: ...
    def add_related_update(
        self, model: Any, field: Any, value: Any
    ) -> None: ...
    def get_related_updates(self) -> List[Any]: ...

class InsertQuery(Query):
    alias_map: collections.OrderedDict
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
    model: Type[django.db.models.base.Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    subquery: bool
    table_map: Dict[Any, Any]
    used_aliases: Set[Any]
    values_select: Tuple
    where: django.db.models.sql.where.WhereNode
    where_class: Type[django.db.models.sql.where.WhereNode]
    compiler: str = ...
    fields: Union[
        List[django.db.models.fields.Field],
        django.utils.datastructures.ImmutableList,
    ] = ...
    objs: List[django.db.models.base.Model] = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    raw: bool = ...
    def insert_values(
        self,
        fields: Union[List[Field], ImmutableList],
        objs: List[Model],
        raw: bool = ...,
    ) -> None: ...

class AggregateQuery(Query):
    alias_map: collections.OrderedDict
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
    model: Type[django.db.models.base.Model]
    order_by: Tuple
    select: Tuple
    select_for_update: bool
    select_for_update_nowait: bool
    select_for_update_of: Tuple
    select_for_update_skip_locked: bool
    select_related: bool
    standard_ordering: bool
    sub_params: Tuple
    subquery: Union[bool, str]
    table_map: Dict[Any, Any]
    used_aliases: Set[Any]
    values_select: Tuple
    where: django.db.models.sql.where.WhereNode
    where_class: Type[django.db.models.sql.where.WhereNode]
    compiler: str = ...
    def add_subquery(self, query: Query, using: str) -> None: ...
