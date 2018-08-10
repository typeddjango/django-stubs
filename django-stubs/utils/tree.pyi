from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union
from uuid import UUID

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import Model
from django.db.models.expressions import (Case, Combinable, CombinedExpression,
                                          F, Subquery)
from django.db.models.functions.datetime import (Extract, Now, Trunc,
                                                 TruncDate, TruncDay,
                                                 TruncHour, TruncMinute,
                                                 TruncMonth, TruncSecond,
                                                 TruncTime, TruncWeek,
                                                 TruncYear)
from django.db.models.functions.text import Chr, Length, Ord, Substr, Upper
from django.db.models.lookups import (BuiltinLookup, FieldGetDbPrepValueMixin,
                                      Lookup)
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q, QueryWrapper
from django.db.models.sql.query import Query
from django.db.models.sql.where import (ExtraWhere, NothingNode,
                                        SubqueryConstraint, WhereNode)
from django.utils.functional import SimpleLazyObject


class Node:
    default: str = ...
    children: Union[
        List[Tuple[str, int]],
        List[
            Union[
                django.db.models.lookups.BuiltinLookup,
                django.db.models.sql.where.WhereNode,
            ]
        ],
    ] = ...
    connector: str = ...
    negated: bool = ...
    def __init__(
        self,
        children: Optional[
            Union[
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
                                    List[Union[Model, int]],
                                    List[Union[CombinedExpression, F]],
                                    List[Union[int, str]],
                                    List[datetime],
                                    List[Group],
                                    List[Permission],
                                    List[User],
                                    List[ContentType],
                                    List[Model],
                                    List[CombinedExpression],
                                    List[F],
                                    List[int],
                                    List[str],
                                    Set[Any],
                                    Set[Optional[int]],
                                    Set[ContentType],
                                    Set[int],
                                    Set[str],
                                    Set[UUID],
                                    Tuple,
                                    bytes,
                                    date,
                                    timedelta,
                                    Decimal,
                                    Model,
                                    Case,
                                    CombinedExpression,
                                    F,
                                    Subquery,
                                    django.db.models.functions.Extract,
                                    django.db.models.functions.Now,
                                    django.db.models.functions.Trunc,
                                    django.db.models.functions.TruncDate,
                                    django.db.models.functions.TruncDay,
                                    django.db.models.functions.TruncHour,
                                    django.db.models.functions.TruncMinute,
                                    django.db.models.functions.TruncMonth,
                                    django.db.models.functions.TruncSecond,
                                    django.db.models.functions.TruncTime,
                                    django.db.models.functions.TruncWeek,
                                    django.db.models.functions.TruncYear,
                                    Chr,
                                    Length,
                                    Ord,
                                    Substr,
                                    Upper,
                                    QuerySet,
                                    Query,
                                    SimpleLazyObject,
                                    float,
                                    frozenset,
                                    int,
                                    range,
                                    str,
                                    UUID,
                                ]
                            ],
                        ],
                        BuiltinLookup,
                    ]
                ],
                List[Union[Tuple[str, str], Q]],
                List[Union[FieldGetDbPrepValueMixin, Node]],
                List[Union[NothingNode, WhereNode]],
            ]
        ] = ...,
        connector: Optional[str] = ...,
        negated: bool = ...,
    ) -> None: ...
    def __deepcopy__(self, memodict: Dict[Any, Any]) -> Node: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __contains__(self, other: Tuple[str, int]) -> bool: ...
    def __eq__(
        self,
        other: Union[
            Tuple[
                str,
                Union[
                    List[Any],
                    Tuple[Union[int, str]],
                    date,
                    Decimal,
                    Model,
                    Combinable,
                    QuerySet,
                    float,
                    int,
                    str,
                ],
            ],
            BuiltinLookup,
            ExtraWhere,
            NothingNode,
            Node,
        ],
    ) -> bool: ...
    def __hash__(self) -> int: ...
    def add(
        self,
        data: Union[
            Tuple[str, int],
            Lookup,
            QueryWrapper,
            ExtraWhere,
            NothingNode,
            SubqueryConstraint,
            Node,
        ],
        conn_type: str,
        squash: bool = ...,
    ) -> Union[
        Tuple[str, int],
        Lookup,
        QueryWrapper,
        ExtraWhere,
        NothingNode,
        SubqueryConstraint,
        Node,
    ]: ...
    def negate(self) -> None: ...
