from collections.abc import Sequence
from typing import Any, ClassVar

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Combinable, Func
from django.db.models.fields import IntegerField
from django.db.models.functions.mixins import FixDurationInputMixin, NumericOutputFieldMixin
from django.db.models.query import _OrderByFieldName
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType

class Aggregate(Func):
    name: str | None
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

class AnyValue(Aggregate):
    def as_sql(  # type: ignore[override]
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any
    ) -> _AsSqlType: ...

class Avg(FixDurationInputMixin, NumericOutputFieldMixin, Aggregate): ...

class Count(Aggregate):
    output_field: ClassVar[IntegerField]

class Max(Aggregate): ...
class Min(Aggregate): ...
class StdDev(NumericOutputFieldMixin, Aggregate): ...

class StringAgg(Aggregate):
    def __init__(self, expression: Combinable | str, delimiter: str | Combinable, **extra: Any) -> None: ...
    def as_mysql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

class Sum(FixDurationInputMixin, Aggregate): ...
class Variance(NumericOutputFieldMixin, Aggregate): ...

__all__ = ["Aggregate", "AnyValue", "Avg", "Count", "Max", "Min", "StdDev", "StringAgg", "Sum", "Variance"]
