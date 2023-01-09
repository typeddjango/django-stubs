import datetime
from collections.abc import Callable, Iterable, Iterator, Sequence
from decimal import Decimal
from typing import Any, TypeVar

from _typeshed import Self
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Q
from django.db.models.fields import Field
from django.db.models.lookups import Lookup, Transform
from django.db.models.query import QuerySet
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from django.db.models.sql.query import Query
from typing_extensions import Literal, TypeAlias

class SQLiteNumericMixin:
    def as_sqlite(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

_Numeric: TypeAlias = float | Decimal

class Combinable:
    ADD: str
    SUB: str
    MUL: str
    DIV: str
    POW: str
    MOD: str
    BITAND: str
    BITOR: str
    BITLEFTSHIFT: str
    BITRIGHTSHIFT: str
    BITXOR: str
    def __neg__(self) -> CombinedExpression: ...
    def __add__(self, other: datetime.timedelta | Combinable | _Numeric | str | None) -> CombinedExpression: ...
    def __sub__(self, other: datetime.timedelta | Combinable | _Numeric) -> CombinedExpression: ...
    def __mul__(self, other: datetime.timedelta | Combinable | _Numeric) -> CombinedExpression: ...
    def __truediv__(self, other: Combinable | _Numeric) -> CombinedExpression: ...
    def __mod__(self, other: int | Combinable) -> CombinedExpression: ...
    def __pow__(self, other: _Numeric | Combinable) -> CombinedExpression: ...
    def __and__(self, other: Combinable | Q) -> Q: ...
    def bitand(self, other: int) -> CombinedExpression: ...
    def bitleftshift(self, other: int) -> CombinedExpression: ...
    def bitrightshift(self, other: int) -> CombinedExpression: ...
    def bitxor(self, other: int) -> CombinedExpression: ...
    def __or__(self, other: Combinable | Q) -> Q: ...
    def bitor(self, other: int) -> CombinedExpression: ...
    def __radd__(self, other: datetime.datetime | _Numeric | Combinable | None) -> CombinedExpression: ...
    def __rsub__(self, other: _Numeric | Combinable) -> CombinedExpression: ...
    def __rmul__(self, other: _Numeric | Combinable) -> CombinedExpression: ...
    def __rtruediv__(self, other: _Numeric | Combinable) -> CombinedExpression: ...
    def __rmod__(self, other: int | Combinable) -> CombinedExpression: ...
    def __rpow__(self, other: _Numeric | Combinable) -> CombinedExpression: ...
    def __rand__(self, other: Any) -> Combinable: ...
    def __ror__(self, other: Any) -> Combinable: ...

class BaseExpression:
    is_summary: bool
    filterable: bool
    window_compatible: bool
    def __init__(self, output_field: Field | None = ...) -> None: ...
    def get_db_converters(self, connection: BaseDatabaseWrapper) -> list[Callable]: ...
    def get_source_expressions(self) -> list[Any]: ...
    def set_source_expressions(self, exprs: Sequence[Combinable]) -> None: ...
    @property
    def contains_aggregate(self) -> bool: ...
    @property
    def contains_over_clause(self) -> bool: ...
    @property
    def contains_column_references(self) -> bool: ...
    def resolve_expression(
        self: Self,
        query: Any = ...,
        allow_joins: bool = ...,
        reuse: set[str] | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> Self: ...
    @property
    def conditional(self) -> bool: ...
    @property
    def field(self) -> Field: ...
    @property
    def output_field(self) -> Field: ...
    @property
    def convert_value(self) -> Callable: ...
    def get_lookup(self, lookup: str) -> type[Lookup] | None: ...
    def get_transform(self, name: str) -> type[Transform] | None: ...
    def relabeled_clone(self: Self, change_map: dict[str | None, str]) -> Self: ...
    def copy(self: Self) -> Self: ...
    def get_group_by_cols(self: Self, alias: str | None = ...) -> list[Self]: ...
    def get_source_fields(self) -> list[Field | None]: ...
    def asc(
        self,
        *,
        descending: bool = ...,
        nulls_first: bool = ...,
        nulls_last: bool = ...,
    ) -> OrderBy: ...
    def desc(
        self,
        *,
        nulls_first: bool = ...,
        nulls_last: bool = ...,
    ) -> OrderBy: ...
    def reverse_ordering(self) -> BaseExpression: ...
    def flatten(self) -> Iterator[BaseExpression]: ...
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def deconstruct(self) -> Any: ...  # fake

class Expression(BaseExpression, Combinable): ...

class CombinedExpression(SQLiteNumericMixin, Expression):
    connector: str
    lhs: Combinable
    rhs: Combinable
    def __init__(self, lhs: Combinable, connector: str, rhs: Combinable, output_field: Field | None = ...) -> None: ...

class DurationExpression(CombinedExpression):
    def compile(self, side: Combinable, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class TemporalSubtraction(CombinedExpression):
    def __init__(self, lhs: Combinable, rhs: Combinable) -> None: ...

class F(Combinable):
    name: str
    def __init__(self, name: str) -> None: ...
    def resolve_expression(
        self,
        query: Any = ...,
        allow_joins: bool = ...,
        reuse: set[str] | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> F: ...
    def asc(
        self,
        *,
        descending: bool = ...,
        nulls_first: bool = ...,
        nulls_last: bool = ...,
    ) -> OrderBy: ...
    def desc(
        self,
        *,
        nulls_first: bool = ...,
        nulls_last: bool = ...,
    ) -> OrderBy: ...
    def deconstruct(self) -> Any: ...  # fake

class ResolvedOuterRef(F): ...

class OuterRef(F):
    def __init__(self, name: str | OuterRef) -> None: ...
    contains_aggregate: bool
    def relabeled_clone(self: Self, relabels: Any) -> Self: ...

class Func(SQLiteNumericMixin, Expression):
    function: str
    name: str
    template: str
    arg_joiner: str
    arity: int | None
    source_expressions: list[Expression]
    extra: dict[Any, Any]
    def __init__(self, *expressions: Any, output_field: Field | None = ..., **extra: Any) -> None: ...
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: BaseDatabaseWrapper,
        function: str | None = ...,
        template: str | None = ...,
        arg_joiner: str | None = ...,
        **extra_context: Any,
    ) -> _AsSqlType: ...

class Value(Expression):
    value: Any
    def __init__(self, value: Any, output_field: Field | None = ...) -> None: ...

class RawSQL(Expression):
    params: list[Any]
    sql: str
    def __init__(self, sql: str, params: Sequence[Any], output_field: Field | None = ...) -> None: ...

class Star(Expression): ...

class Col(Expression):
    target: Field
    alias: str
    contains_column_references: Literal[True]
    possibly_multivalued: Literal[False]
    def __init__(self, alias: str, target: Field, output_field: Field | None = ...) -> None: ...

class Ref(Expression):
    def __init__(self, refs: str, source: Expression) -> None: ...

class ExpressionList(Func):
    def __init__(self, *expressions: BaseExpression | Combinable, **extra: Any) -> None: ...

class OrderByList(Func): ...

class ExpressionWrapper(Expression):
    def __init__(self, expression: Q | Combinable, output_field: Field) -> None: ...

class When(Expression):
    template: str
    condition: Any
    result: Any
    def __init__(self, condition: Any = ..., then: Any = ..., **lookups: Any) -> None: ...

class Case(Expression):
    template: str
    case_joiner: str
    cases: Any
    default: Any
    extra: Any
    def __init__(
        self, *cases: Any, default: Any | None = ..., output_field: Field | None = ..., **extra: Any
    ) -> None: ...

class Subquery(BaseExpression, Combinable):
    template: str
    query: Query
    extra: dict[Any, Any]
    def __init__(self, queryset: Query | QuerySet, output_field: Field | None = ..., **extra: Any) -> None: ...

class Exists(Subquery):
    negated: bool
    def __init__(self, queryset: Query | QuerySet, negated: bool = ..., **kwargs: Any) -> None: ...
    def __invert__(self) -> Exists: ...

class OrderBy(Expression):
    template: str
    nulls_first: bool
    nulls_last: bool
    descending: bool
    expression: Expression | F | Subquery
    def __init__(
        self,
        expression: Expression | F | Subquery,
        descending: bool = ...,
        nulls_first: bool = ...,
        nulls_last: bool = ...,
    ) -> None: ...

class Window(SQLiteNumericMixin, Expression):
    template: str
    contains_aggregate: bool
    contains_over_clause: bool
    partition_by: ExpressionList | None
    order_by: ExpressionList | None
    def __init__(
        self,
        expression: BaseExpression,
        partition_by: str | Iterable[BaseExpression | F] | F | BaseExpression | None = ...,
        order_by: Sequence[BaseExpression | F] | BaseExpression | F | None = ...,
        frame: WindowFrame | None = ...,
        output_field: Field | None = ...,
    ) -> None: ...

class WindowFrame(Expression):
    template: str
    frame_type: str
    def __init__(self, start: int | None = ..., end: int | None = ...) -> None: ...
    def window_frame_start_end(
        self, connection: BaseDatabaseWrapper, start: int | None, end: int | None
    ) -> tuple[int, int]: ...

class RowRange(WindowFrame): ...
class ValueRange(WindowFrame): ...
