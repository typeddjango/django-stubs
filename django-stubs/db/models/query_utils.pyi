from collections import OrderedDict
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import F
from django.db.models.fields import (
    DateTimeCheckMixin,
    Field,
)
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.lookups import (
    Lookup,
    Transform,
)
from django.db.models.options import Options
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)


def check_rel_lookup_compatibility(
    model: Type[Model],
    target_opts: Options,
    field: Union[ManyToOneRel, ForeignKey]
) -> bool: ...


def refs_expression(lookup_parts: List[str], annotations: OrderedDict) -> Any: ...


def select_related_descend(
    field: Union[Field, DateTimeCheckMixin],
    restricted: bool,
    requested: Any,
    load_fields: Optional[Set[str]],
    reverse: bool = ...
) -> bool: ...


def subclasses(
    cls: Type[Union[Field, Transform]]
) -> Iterator[Type[Union[Field, Transform]]]: ...


class DeferredAttribute:
    def __get__(
        self,
        instance: Optional[Model],
        cls: Type[Model] = ...
    ) -> Optional[Union[str, int, DeferredAttribute]]: ...
    def __init__(self, field_name: str) -> None: ...
    def _check_parent_chain(self, instance: Model, name: str) -> None: ...


class FilteredRelation:
    def __eq__(self, other: FilteredRelation) -> bool: ...
    def __init__(self, relation_name: str, *, condition = ...) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[str]], Tuple[str, List[Any]], Tuple[str, List[Union[int, str]]]]: ...
    def clone(self) -> FilteredRelation: ...


class Q:
    def __and__(self, other: Q) -> Q: ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __invert__(self) -> Q: ...
    def __or__(self, other: Q) -> Q: ...
    def _combine(self, other: Q, conn: str) -> Q: ...
    def deconstruct(
        self
    ) -> Union[Tuple[str, Tuple[Tuple[str, F], Tuple[str, F]], Dict[Any, Any]], Tuple[str, Tuple, Dict[str, F]], Tuple[str, Tuple[Q], Dict[Any, Any]]]: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: Optional[Set[str]] = ...,
        summarize: bool = ...,
        for_save: bool = ...
    ) -> WhereNode: ...


class QueryWrapper:
    def __init__(self, sql: str, params: List[Any]) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler = ...,
        connection: DatabaseWrapper = ...
    ) -> Tuple[str, List[Any]]: ...


class RegisterLookupMixin:
    @classmethod
    def _clear_cached_lookups(cls) -> None: ...
    @classmethod
    def _get_lookup(cls, lookup_name: str) -> Any: ...
    @classmethod
    def _unregister_lookup(
        cls,
        lookup: Type[Union[Lookup, Transform]],
        lookup_name: Optional[str] = ...
    ) -> None: ...
    def get_lookup(self, lookup_name: str) -> Any: ...
    @classmethod
    def get_lookups(cls) -> Dict[str, Type[Union[Lookup, Transform]]]: ...
    def get_transform(self, lookup_name: str) -> object: ...
    @staticmethod
    def merge_dicts(
        dicts: Any
    ) -> Dict[str, Type[Union[Lookup, Transform]]]: ...
    @classmethod
    def register_lookup(
        cls,
        lookup: Type[Union[Lookup, Transform]],
        lookup_name: Optional[str] = ...
    ) -> Type[Union[Lookup, Transform]]: ...