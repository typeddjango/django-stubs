from django.db.models.base import Model
from django.db.models.sql.where import WhereNode
from typing import (
    Set,
    Tuple,
    Type,
    Union,
)


class JoinPromoter:
    def __init__(self, connector: str, num_children: int, negated: bool) -> None: ...
    def add_votes(self, votes: Union[Set[str], Tuple]) -> None: ...
    def update_join_types(self, query: Query) -> Set[str]: ...


class Query:
    def __init__(
        self,
        model: Type[Model],
        where: Type[WhereNode] = ...
    ) -> None: ...