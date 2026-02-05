from collections.abc import Sequence
from typing import Any, ClassVar

from django.db.models.expressions import BaseExpression, Combinable, OrderByList

class OrderableAggMixin:
    allow_order_by: ClassVar[bool]
    order_by: OrderByList
    def __init__(
        self,
        *expressions: BaseExpression | Combinable | str,
        ordering: Sequence[str] = ...,
        order_by: Sequence[str] = ...,
        **extra: Any,
    ) -> None: ...
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None: ...
