from collections.abc import Sequence

from django.db.models import Deferrable
from django.db.models.constraints import BaseConstraint
from django.db.models.expressions import Combinable
from django.db.models.query_utils import Q

class ExclusionConstraint(BaseConstraint):
    expressions: Sequence[tuple[str | Combinable, str]]
    index_type: str
    condition: Q | None
    def __init__(
        self,
        *,
        name: str,
        expressions: Sequence[tuple[str | Combinable, str]],
        index_type: str | None = ...,
        condition: Q | None = ...,
        deferrable: Deferrable | None = ...,
        include: list[str] | tuple[str] | None = ...,
        opclasses: list[str] | tuple[str] = ...,
        violation_error_message: str | None = ...
    ) -> None: ...
