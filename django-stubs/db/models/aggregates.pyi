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
    # An aggregate over no rows is NULL, so without a `default` the value can be `None`.
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
    # A `default` wraps the aggregate in `Coalesce`, so the value keeps the output field's type.
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
    @overload
    def __init__(
        self,
        *expressions: Any,
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

# mypy and pyright don't solve a subclass's type parameters from an inherited self-annotated overload,
# so subclasses that take `Aggregate.__init__` repeat its overloads to type `output_field` and `default`.
# pyrefly and ty get it right from the inherited overloads alone.
# TODO: drop the repeated overloads once mypy and pyright support it,
# see https://github.com/python/mypy/issues/22395 and https://github.com/microsoft/pyright/issues/11989.
class AnyValue(Aggregate[_OutputField]):
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
    @overload
    def __init__(
        self,
        *expressions: Any,
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
    @overload
    def __init__(
        self,
        *expressions: Any,
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
    @overload
    def __init__(
        self,
        *expressions: Any,
        distinct: bool = False,
        filter: Q | BaseExpression | None = None,
        default: Any | None = None,
        order_by: _OrderByFieldName | Sequence[_OrderByFieldName] | None = None,
        **extra: Any,
    ) -> None: ...

class Min(Aggregate[_OutputField]):
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
    @overload
    def __init__(
        self,
        *expressions: Any,
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
    @overload
    def __init__(
        self,
        *expressions: Any,
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
