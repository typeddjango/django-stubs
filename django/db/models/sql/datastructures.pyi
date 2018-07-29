from collections import OrderedDict
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.fields.related import ForeignObject
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.query_utils import (
    FilteredRelation,
    PathInfo,
)
from django.db.models.sql.compiler import SQLCompiler
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class BaseTable:
    def __init__(self, table_name: str, alias: Optional[str]) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...
    def equals(self, other: Join, with_filtered_relation: bool) -> bool: ...
    def relabeled_clone(self, change_map: OrderedDict) -> BaseTable: ...


class Join:
    def __eq__(
        self,
        other: Union[BaseTable, Join]
    ) -> bool: ...
    def __init__(
        self,
        table_name: str,
        parent_alias: str,
        table_alias: Optional[str],
        join_type: str,
        join_field: Union[ForeignObjectRel, ForeignObject],
        nullable: bool,
        filtered_relation: Optional[FilteredRelation] = ...
    ) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[str]], Tuple[str, List[Any]]]: ...
    def demote(self) -> Join: ...
    def equals(
        self,
        other: Union[BaseTable, Join],
        with_filtered_relation: bool
    ) -> bool: ...
    def promote(self) -> Join: ...
    def relabeled_clone(
        self,
        change_map: Union[OrderedDict, Dict[str, str]]
    ) -> Join: ...


class MultiJoin:
    def __init__(
        self,
        names_pos: int,
        path_with_names: List[Tuple[str, List[PathInfo]]]
    ) -> None: ...