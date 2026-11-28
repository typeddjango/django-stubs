from collections.abc import Sequence
from typing import Any, ClassVar, overload

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import BaseExpression, Combinable, Func, _OutputField
from django.db.models.fields import Field, IntegerField
from django.db.models.functions.mixins import FixDurationInputMixin, NumericOutputFieldMixin
from django.db.models.query import _OrderByFieldName
from django.db.models.query_utils import Q
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from typing_extensions import TypeVar, override

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Aggregate(Func[_OutputField]):
    name: str | None
    filter: Any
    allow_distinct: bool
    allow_order_by: bool
    empty_result_set_value: int | None
    # `Aggregate("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: Aggregate[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Aggregate("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: Aggregate[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Aggregate("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    @property
    def default_alias(self) -> str: ...
    @override
    def as_sql(  # type: ignore[override]
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any
    ) -> _AsSqlType: ...

class AnyValue(Aggregate[_OutputField]):
    # `AnyValue("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: AnyValue[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `AnyValue("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: AnyValue[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `AnyValue("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    @override
    def as_sql(  # type: ignore[override]
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any
    ) -> _AsSqlType: ...

class Avg(FixDurationInputMixin, NumericOutputFieldMixin, Aggregate[_OutputField]):
    # `Avg("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: Avg[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Avg("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: Avg[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Avg("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class BitAggregate(Aggregate):
    def __init__(self, expression: Combinable | str, **extra: Any) -> None: ...
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

class BitAnd(BitAggregate): ...
class BitOr(BitAggregate): ...
class BitXor(BitAggregate): ...

class Count(Aggregate):
    output_field: ClassVar[IntegerField]
    def __init__(
        self,
        expression: Combinable | str,
        filter: Q | BaseExpression | None = None,
        *,
        distinct: bool = False,
        **extra: Any,
    ) -> None: ...

class Max(Aggregate[_OutputField]):
    # `Max("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: Max[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Max("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: Max[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Max("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class Min(Aggregate[_OutputField]):
    # `Min("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: Min[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Min("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: Min[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Min("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class StdDev(NumericOutputFieldMixin, Aggregate):
    def __init__(
        self,
        expression: Combinable | str,
        sample: bool = False,
        *,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        **extra: Any,
    ) -> None: ...

class StringAgg(Aggregate):
    def __init__(
        self,
        expression: Combinable | str,
        delimiter: str | Combinable,
        *,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...
    def as_mysql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...
    @override
    def as_sqlite(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

class Sum(FixDurationInputMixin, Aggregate[_OutputField]):
    # `Sum("price", output_field=IntegerField())`: an aggregate over no rows returns `None`.
    @overload
    def __init__(
        self: Sum[Field[_ST, _GT | None]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Sum("price", output_field=IntegerField(), default=0)`: `default` replaces `None`.
    @overload
    def __init__(
        self: Sum[Field[_ST, _GT]],
        *expressions: Any,
        output_field: Field[_ST, _GT],
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: object,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...
    # `Sum("price")` or `output_field=None`: the type can't be inferred, so it stays `Field`.
    @overload
    def __init__(
        self,
        *expressions: Any,
        output_field: Field | None = None,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class Variance(NumericOutputFieldMixin, Aggregate):
    def __init__(
        self,
        expression: Combinable | str,
        sample: bool = False,
        *,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        **extra: Any,
    ) -> None: ...

__all__ = [
    "Aggregate",
    "AnyValue",
    "Avg",
    "BitAnd",
    "BitOr",
    "BitXor",
    "Count",
    "Max",
    "Min",
    "StdDev",
    "StringAgg",
    "Sum",
    "Variance",
]
