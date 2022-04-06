import sys
from collections import namedtuple
from typing import (
    Any,
    Collection,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.lookups import Lookup, Transform
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.utils import tree

PathInfo = namedtuple(
    "PathInfo", ["from_opts", "to_opts", "target_fields", "join_field", "m2m", "direct", "filtered_relation"]
)

class InvalidQuery(Exception): ...

def subclasses(cls: Type[RegisterLookupMixin]) -> Iterator[Type[RegisterLookupMixin]]: ...

class Q(tree.Node):
    AND: str = ...
    OR: str = ...
    conditional: bool = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    # Fake signature, the real is
    # def __init__(self, *args: Any, _connector: Optional[Any] = ..., _negated: bool = ..., **kwargs: Any) -> None: ...
    def __or__(self, other: Q) -> Q: ...
    def __and__(self, other: Q) -> Q: ...
    def __invert__(self) -> Q: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: Optional[Set[str]] = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> WhereNode: ...
    def deconstruct(self) -> Tuple[str, Tuple, Dict[str, str]]: ...

class DeferredAttribute:
    field_name: str = ...
    field: Field
    def __init__(self, field: Field) -> None: ...

_R = TypeVar("_R", bound=Type)

class RegisterLookupMixin:
    class_lookups: List[Dict[Any, Any]]
    lookup_name: str
    @classmethod
    def get_lookups(cls) -> Dict[str, Any]: ...
    def get_lookup(self, lookup_name: str) -> Optional[Type[Lookup]]: ...
    def get_transform(self, lookup_name: str) -> Optional[Type[Transform]]: ...
    @staticmethod
    def merge_dicts(dicts: Iterable[Dict[str, Any]]) -> Dict[str, Any]: ...
    @classmethod
    def register_lookup(cls, lookup: _R, lookup_name: Optional[str] = ...) -> _R: ...
    @classmethod
    def _unregister_lookup(cls, lookup: Type[Lookup], lookup_name: Optional[str] = ...) -> None: ...

def select_related_descend(
    field: Field,
    restricted: bool,
    requested: Optional[Mapping[str, Any]],
    load_fields: Optional[Collection[str]],
    reverse: bool = ...,
) -> bool: ...

_E = TypeVar("_E", bound=BaseExpression)

def refs_expression(
    lookup_parts: Sequence[str], annotations: Mapping[str, _E]
) -> Tuple[Union[Literal[False], _E], Sequence[str]]: ...
def check_rel_lookup_compatibility(model: Type[Model], target_opts: Any, field: FieldCacheMixin) -> bool: ...

class FilteredRelation:
    relation_name: str = ...
    alias: Optional[str] = ...
    condition: Q = ...
    path: List[str] = ...
    def __init__(self, relation_name: str, *, condition: Q = ...) -> None: ...
    def clone(self) -> FilteredRelation: ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> None: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> Any: ...
