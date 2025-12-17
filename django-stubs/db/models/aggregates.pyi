from collections.abc import Sequence
from typing import Any, ClassVar

from django.db.models.expressions import Combinable, Func
from django.db.models.fields import IntegerField
from django.db.models.functions.mixins import FixDurationInputMixin, NumericOutputFieldMixin
from django.db.models.query import _OrderByFieldName

class Aggregate(Func):
    filter_template: str
    filter: Any
    allow_distinct: bool
    allow_order_by: bool
    empty_result_set_value: int | None
    def __init__(
        self,
        *expressions: Any,
        distinct: bool = False,
        filter: Any | None = None,
        default: Any | None = None,
        order_by: Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class Avg(FixDurationInputMixin, NumericOutputFieldMixin, Aggregate): ...

class Count(Aggregate):
    output_field: ClassVar[IntegerField]

class Max(Aggregate): ...
class Min(Aggregate): ...
class StdDev(NumericOutputFieldMixin, Aggregate): ...

class StringAgg(Aggregate):
    def __init__(self, expression: Combinable | str, delimiter: str | Combinable, **extra: Any) -> None: ...

class Sum(FixDurationInputMixin, Aggregate): ...
class Variance(NumericOutputFieldMixin, Aggregate): ...

__all__ = ["Aggregate", "Avg", "Count", "Max", "Min", "StdDev", "Sum", "Variance"]
