from django.db.models.sql.where import WhereNode
from typing import (
    Any,
    Set,
    Tuple,
    Type,
    Union,
)


class JoinPromoter:
    def __init__(self, connector: str, num_children: int, negated: bool) -> None: ...
    def add_votes(self, votes: Union[Tuple, Set[str]]) -> None: ...
    def update_join_types(self, query: Query) -> Set[str]: ...


class Query:
    def __init__(self, model: Any, where: Type[WhereNode] = ...) -> None: ...