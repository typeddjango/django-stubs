from collections import OrderedDict, namedtuple
from datetime import date
from decimal import Decimal
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Type, Union

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import Expression, F
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.lookups import Lookup, Transform
from django.db.models.options import Options
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.utils import tree

PathInfo = namedtuple(
    "PathInfo",
    "from_opts to_opts target_fields join_field m2m direct filtered_relation",
)

class InvalidQuery(Exception): ...

def subclasses(
    cls: Type[Union[Field, Transform]]
) -> Iterator[Type[Union[Field, Transform]]]: ...

class QueryWrapper:
    contains_aggregate: bool = ...
    data: Tuple[str, List[Any]] = ...
    def __init__(self, sql: str, params: List[Any]) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler = ..., connection: DatabaseWrapper = ...
    ) -> Tuple[str, List[Any]]: ...

class Q(tree.Node):
    children: Union[
        List[Dict[str, str]],
        List[
            Union[
                Tuple[
                    str,
                    Optional[
                        Union[
                            Any,
                            Dict[Any, Any],
                            Iterator[Any],
                            List[Any],
                            List[Dict[str, str]],
                            List[List[str]],
                            List[None],
                            List[Union[django.db.models.base.Model, int]],
                            List[
                                Union[
                                    django.db.models.expressions.CombinedExpression,
                                    django.db.models.expressions.F,
                                ]
                            ],
                            List[Union[int, str]],
                            List[datetime.datetime],
                            List[django.contrib.auth.models.Group],
                            List[django.contrib.auth.models.Permission],
                            List[django.contrib.auth.models.User],
                            List[
                                django.contrib.contenttypes.models.ContentType
                            ],
                            List[django.db.models.base.Model],
                            List[
                                django.db.models.expressions.CombinedExpression
                            ],
                            List[django.db.models.expressions.F],
                            List[int],
                            List[str],
                            Set[Any],
                            Set[Optional[int]],
                            Set[django.contrib.contenttypes.models.ContentType],
                            Set[int],
                            Set[str],
                            Set[uuid.UUID],
                            Tuple,
                            bytes,
                            datetime.date,
                            datetime.timedelta,
                            decimal.Decimal,
                            django.db.models.base.Model,
                            django.db.models.expressions.Case,
                            django.db.models.expressions.CombinedExpression,
                            django.db.models.expressions.F,
                            django.db.models.expressions.Subquery,
                            django.db.models.functions.datetime.Extract,
                            django.db.models.functions.datetime.Now,
                            django.db.models.functions.datetime.Trunc,
                            django.db.models.functions.datetime.TruncDate,
                            django.db.models.functions.datetime.TruncDay,
                            django.db.models.functions.datetime.TruncHour,
                            django.db.models.functions.datetime.TruncMinute,
                            django.db.models.functions.datetime.TruncMonth,
                            django.db.models.functions.datetime.TruncSecond,
                            django.db.models.functions.datetime.TruncTime,
                            django.db.models.functions.datetime.TruncWeek,
                            django.db.models.functions.datetime.TruncYear,
                            django.db.models.functions.text.Chr,
                            django.db.models.functions.text.Length,
                            django.db.models.functions.text.Ord,
                            django.db.models.functions.text.Substr,
                            django.db.models.functions.text.Upper,
                            django.db.models.query.QuerySet,
                            django.db.models.sql.query.Query,
                            django.utils.functional.SimpleLazyObject,
                            float,
                            frozenset,
                            int,
                            range,
                            str,
                            uuid.UUID,
                        ]
                    ],
                ],
                django.db.models.query_utils.Q,
            ]
        ],
    ]
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
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: Optional[Set[str]] = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> WhereNode: ...
    def deconstruct(
        self
    ) -> Tuple[
        str, Tuple, Union[Dict[str, Union[bool, F]], Dict[str, str]]
    ]: ...

class DeferredAttribute:
    field_name: str = ...
    def __init__(self, field_name: str) -> None: ...
    def __get__(
        self, instance: Optional[Model], cls: Type[Model] = ...
    ) -> Optional[Union[date, Decimal, DeferredAttribute, float, int, str]]: ...

class RegisterLookupMixin:
    @classmethod
    def get_lookups(cls) -> Dict[str, Type[Union[Lookup, Transform]]]: ...
    def get_lookup(self, lookup_name: str) -> Optional[Type[Lookup]]: ...
    def get_transform(self, lookup_name: str) -> Optional[Type[Transform]]: ...
    @staticmethod
    def merge_dicts(
        dicts: List[Dict[str, Type[Union[Lookup, Transform]]]]
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
            bool,
        ]
    ],
    load_fields: Optional[Set[str]],
    reverse: bool = ...,
) -> bool: ...
def refs_expression(
    lookup_parts: List[str], annotations: OrderedDict
) -> Union[
    Tuple[List[str], List[str]],
    Tuple[bool, Tuple],
    Tuple[Expression, List[Any]],
]: ...
def check_rel_lookup_compatibility(
    model: Type[Model], target_opts: Options, field: FieldCacheMixin
) -> bool: ...

class FilteredRelation:
    relation_name: str = ...
    alias: Optional[str] = ...
    condition: django.db.models.query_utils.Q = ...
    path: List[str] = ...
    def __init__(self, relation_name: str, *, condition: Any = ...) -> None: ...
    def __eq__(self, other: FilteredRelation) -> bool: ...
    def clone(self) -> FilteredRelation: ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> None: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Union[int, str]]]: ...
