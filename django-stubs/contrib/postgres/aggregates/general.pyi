from typing import ClassVar

from django.contrib.postgres.fields import ArrayField
from django.db.models import Aggregate, BooleanField, JSONField, TextField

from .mixins import OrderableAggMixin

class ArrayAgg(OrderableAggMixin, Aggregate):
    @property
    def output_field(self) -> ArrayField: ...  # type: ignore[override]

class BitAnd(Aggregate): ...
class BitOr(Aggregate): ...

class BoolAnd(Aggregate):
    output_field: ClassVar[BooleanField]  # type: ignore[assignment]

class BoolOr(Aggregate):
    output_field: ClassVar[BooleanField]  # type: ignore[assignment]

class JSONBAgg(OrderableAggMixin, Aggregate):
    output_field: ClassVar[JSONField]  # type: ignore[assignment]

class StringAgg(OrderableAggMixin, Aggregate):
    output_field: ClassVar[TextField]  # type: ignore[assignment]
