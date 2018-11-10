from typing import Any, Dict, List, Optional, Tuple, Union

from django.contrib.auth.models import User
from django.db.models.fields.related_lookups import RelatedLookupMixin
from django.db.models.lookups import BuiltinLookup, FieldGetDbPrepValueMixin
from django.db.models.sql.where import ExtraWhere, NothingNode


class Node:
    default: str = ...
    children: Union[
        List[Tuple[str, int]], List[django.db.models.lookups.Contains]
    ] = ...
    connector: str = ...
    negated: bool = ...
    def __init__(
        self,
        children: Optional[
            Union[
                List[Dict[str, str]],
                List[Tuple[str, List[User]]],
                List[RelatedLookupMixin],
                List[BuiltinLookup],
                List[FieldGetDbPrepValueMixin],
                List[NothingNode],
                List[Node],
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
            Tuple[str, List[Any]], BuiltinLookup, ExtraWhere, NothingNode, Node
        ],
    ) -> bool: ...
    def __hash__(self) -> int: ...
    def add(self, data: Any, conn_type: str, squash: bool = ...) -> Any: ...
    def negate(self) -> None: ...
