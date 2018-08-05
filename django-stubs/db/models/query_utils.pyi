from collections import OrderedDict, namedtuple
from decimal import Decimal
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Type, Union

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import Expression, F
from django.db.models.fields import CharField, Field, TextField
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.lookups import Lookup, Transform
from django.db.models.options import Options
from django.db.models.sql.compiler import SQLCompiler
from django.utils import tree

PathInfo = namedtuple(
    "PathInfo",
    "from_opts to_opts target_fields join_field m2m direct filtered_relation",
)

class InvalidQuery(Exception): ...

def subclasses(
    cls: Type[Union[TextField, Transform, CharField]]
) -> Iterator[Type[Union[TextField, Transform, CharField]]]: ...

class QueryWrapper:
    contains_aggregate: bool = ...
    data: Tuple[str, List[Any]] = ...
    def __init__(self, sql: str, params: List[Any]) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler = ..., connection: DatabaseWrapper = ...
    ) -> Tuple[str, List[Any]]: ...

class Q(tree.Node):
    children: List
    connector: str
    negated: bool
    AND: str = ...
    OR: str = ...
    default: Any = ...
    conditional: bool = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __or__(self, other: Any) -> Q: ...
    def __and__(self, other: Any) -> Q: ...
    def __invert__(self) -> Q: ...
    def resolve_expression(
        self,
        query: Optional[Any] = ...,
        allow_joins: bool = ...,
        reuse: Optional[Any] = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ): ...
    def deconstruct(
        self
    ) -> Tuple[
        str,
        Tuple,
        Union[
            Dict[str, str],
            Dict[str, Union[F, bool]],
            Dict[str, F],
            Dict[Any, Any],
        ],
    ]: ...

class DeferredAttribute:
    field_name: str = ...
    def __init__(self, field_name: str) -> None: ...
    def __get__(
        self, instance: Optional[Model], cls: Type[Model] = ...
    ) -> Optional[Union[str, Decimal, DeferredAttribute]]: ...

class RegisterLookupMixin:
    @classmethod
    def get_lookups(cls) -> Dict[str, Type[Union[Lookup, Transform]]]: ...
    def get_lookup(self, lookup_name: str) -> Optional[Type[Lookup]]: ...
    def get_transform(self, lookup_name: str) -> Optional[Type[Transform]]: ...
    @staticmethod
    def merge_dicts(
        dicts: List[Dict[str, Type[Union[Transform, Lookup]]]]
    ) -> Dict[str, Type[Union[Lookup, Transform]]]: ...
    @classmethod
    def register_lookup(
        cls,
        lookup: Type[Union[Lookup, Transform]],
        lookup_name: Optional[str] = ...,
    ) -> Type[Union[Lookup, Transform]]: ...

def select_related_descend(
    field: Field,
    restricted: bool,
    requested: Optional[
        Union[
            bool,
            Dict[
                str,
                Dict[
                    str,
                    Dict[
                        str,
                        Dict[
                            str, Dict[str, Dict[str, Dict[str, Dict[Any, Any]]]]
                        ],
                    ],
                ],
            ],
        ]
    ],
    load_fields: Optional[Set[str]],
    reverse: bool = ...,
) -> bool: ...
def refs_expression(
    lookup_parts: List[str], annotations: OrderedDict
) -> Tuple[Expression, List[str]]: ...
def check_rel_lookup_compatibility(
    model: Type[Model], target_opts: Options, field: FieldCacheMixin
) -> bool: ...

class FilteredRelation:
    relation_name: str = ...
    alias: Optional[str] = ...
    condition: django.db.models.query_utils.Q = ...
    path: List[str] = ...
    def __init__(self, relation_name: Any, *, condition: Any = ...) -> None: ...
    def __eq__(self, other: Any): ...
    def clone(self): ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> None: ...
    def as_sql(self, compiler: Any, connection: Any): ...
