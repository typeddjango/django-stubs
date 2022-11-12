from typing import List, Sequence, Tuple

from django.db.models import Deferrable
from django.db.models.constraints import BaseConstraint
from django.db.models.expressions import Combinable
from django.db.models.query_utils import Q

class ExclusionConstraint(BaseConstraint):
    expressions: Sequence[Tuple[str | Combinable, str]]
    index_type: str
    condition: Q | None
    def __init__(
        self,
        *,
        name: str,
        expressions: Sequence[Tuple[str | Combinable, str]],
        index_type: str | None = ...,
        condition: Q | None = ...,
        deferrable: Deferrable | None = ...,
        include: List[str] | Tuple[str] | None = ...,
        opclasses: List[str] | Tuple[str] = ...,
    ) -> None: ...
