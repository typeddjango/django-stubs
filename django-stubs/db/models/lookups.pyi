from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from uuid import UUID

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import (Col, Combinable, Expression, Func,
                                          Ref, Subquery)
from django.db.models.fields import TextField
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.utils.datastructures import OrderedSet


class Lookup:
    lookup_name: Any = ...
    prepare_rhs: bool = ...
    can_use_none_as_rhs: bool = ...
    rhs: Any = ...
    bilateral_transforms: Any = ...
    def __init__(
        self, lhs: Union[Expression, TextField, MultiColSource], rhs: Any
    ) -> None: ...
    def apply_bilateral_transforms(self, value: Expression) -> Transform: ...
    def batch_process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        rhs: Optional[OrderedSet] = ...,
    ) -> Tuple[
        List[str],
        Union[List[Optional[int]], List[Union[Combinable, int]], List[str]],
    ]: ...
    def get_source_expressions(self) -> List[Expression]: ...
    lhs: Any = ...
    def set_source_expressions(self, new_exprs: List[Ref]) -> None: ...
    def get_prep_lookup(self) -> Any: ...
    def get_db_prep_lookup(
        self, value: Union[int, str], connection: DatabaseWrapper
    ) -> Tuple[str, Union[List[int], List[str]]]: ...
    def process_lhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        lhs: Optional[Col] = ...,
    ) -> Tuple[str, Union[List[Union[int, str]], Tuple]]: ...
    def process_rhs(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[
        str,
        Union[
            List[None],
            List[Union[date, str]],
            List[Union[int, str]],
            List[Decimal],
            List[float],
            List[memoryview],
            Tuple,
        ],
    ]: ...
    def rhs_is_direct_value(self) -> bool: ...
    def relabeled_clone(
        self, relabels: Dict[Optional[str], str]
    ) -> Union[BuiltinLookup, FieldGetDbPrepValueMixin]: ...
    def get_group_by_cols(self) -> List[Expression]: ...
    def as_sql(self, compiler: Any, connection: Any) -> None: ...
    def contains_aggregate(self) -> bool: ...
    def contains_over_clause(self) -> bool: ...
    @property
    def is_summary(self): ...

class Transform(RegisterLookupMixin, Func):
    bilateral: bool = ...
    arity: int = ...
    @property
    def lhs(self) -> Expression: ...
    def get_bilateral_transforms(self) -> List[Type[Transform]]: ...

class BuiltinLookup(Lookup):
    def process_lhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        lhs: Optional[Col] = ...,
    ) -> Tuple[str, List[Union[int, str]]]: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[
        str,
        Union[
            List[Optional[int]],
            List[Union[date, str]],
            List[Union[Decimal, int]],
            List[Union[int, str]],
            List[float],
            List[memoryview],
        ],
    ]: ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...

class FieldGetDbPrepValueMixin:
    get_db_prep_lookup_value_is_iterable: bool = ...
    def get_db_prep_lookup(
        self, value: Any, connection: DatabaseWrapper
    ) -> Tuple[
        str,
        Union[
            List[Optional[int]],
            List[Union[Combinable, int]],
            List[Decimal],
            List[float],
            List[memoryview],
            List[str],
        ],
    ]: ...

class FieldGetDbPrepValueIterableMixin(FieldGetDbPrepValueMixin):
    get_db_prep_lookup_value_is_iterable: bool = ...
    def get_prep_lookup(
        self
    ) -> Union[
        List[Optional[int]],
        List[Union[Combinable, int]],
        List[datetime],
        List[Model],
        List[str],
        List[UUID],
        Subquery,
        Query,
    ]: ...
    def process_rhs(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[Tuple, Tuple]: ...
    def resolve_expression_parameter(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        sql: str,
        param: Optional[Union[Combinable, int, str]],
    ) -> Tuple[str, Union[List[None], List[int], List[str]]]: ...
    def batch_process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        rhs: Optional[OrderedSet] = ...,
    ) -> Tuple[Tuple[str], Tuple]: ...

class Exact(FieldGetDbPrepValueMixin, BuiltinLookup):
    bilateral_transforms: List[Type[django.db.models.lookups.Transform]]
    contains_aggregate: bool
    contains_over_clause: bool
    lhs: django.db.models.expressions.Expression
    rhs: Any
    lookup_name: str = ...
    def process_rhs(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[
        str,
        Union[
            List[None],
            List[Union[int, str]],
            List[Decimal],
            List[float],
            List[memoryview],
            Tuple,
        ],
    ]: ...

class IExact(BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Optional[Union[django.db.models.expressions.Col, str]]
    lookup_name: str = ...
    prepare_rhs: bool = ...
    def process_rhs(
        self, qn: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...

class GreaterThan(FieldGetDbPrepValueMixin, BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: Union[
        django.db.models.expressions.Expression,
        django.db.models.expressions.SQLiteNumericMixin,
    ]
    rhs: Any
    lookup_name: str = ...

class GreaterThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: Any
    lookup_name: str = ...

class LessThan(FieldGetDbPrepValueMixin, BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: Any
    lookup_name: str = ...

class LessThanOrEqual(FieldGetDbPrepValueMixin, BuiltinLookup):
    bilateral_transforms: List[Type[django.db.models.lookups.Transform]]
    contains_aggregate: bool
    contains_over_clause: bool
    lhs: Union[
        django.db.models.expressions.Expression,
        django.db.models.expressions.SQLiteNumericMixin,
    ]
    rhs: Union[
        datetime.date,
        decimal.Decimal,
        django.db.models.expressions.Expression,
        float,
    ]
    lookup_name: str = ...

class IntegerFieldFloatRounding:
    rhs: Any = ...
    def get_prep_lookup(self) -> Union[Combinable, Query, int]: ...

class IntegerGreaterThanOrEqual(
    IntegerFieldFloatRounding, GreaterThanOrEqual
): ...
class IntegerLessThan(IntegerFieldFloatRounding, LessThan): ...

class In(FieldGetDbPrepValueIterableMixin, BuiltinLookup):
    bilateral_transforms: List[Type[django.db.models.lookups.Transform]]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: Any
    lookup_name: str = ...
    def process_rhs(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, Tuple]: ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, Union[List[Optional[int]], List[Union[int, str]]]]: ...
    def split_parameter_list_as_sql(self, compiler: Any, connection: Any): ...

class PatternLookup(BuiltinLookup):
    param_pattern: str = ...
    prepare_rhs: bool = ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def process_rhs(
        self, qn: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, Union[List[int], List[str]]]: ...

class Contains(PatternLookup):
    bilateral_transforms: List[Type[django.db.models.lookups.Transform]]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...

class IContains(Contains):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...

class StartsWith(PatternLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...
    param_pattern: str = ...

class IStartsWith(StartsWith):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...

class EndsWith(PatternLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...
    param_pattern: str = ...

class IEndsWith(EndsWith):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: Union[django.db.models.expressions.Expression, str]
    lookup_name: str = ...

class Range(FieldGetDbPrepValueIterableMixin, BuiltinLookup):
    bilateral_transforms: List[Type[django.db.models.lookups.Transform]]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: Union[
        List[Union[django.db.models.expressions.Combinable, int]],
        List[datetime.datetime],
        Tuple[
            Union[django.db.models.expressions.Combinable, int],
            Union[django.db.models.expressions.CombinedExpression, int],
        ],
        Tuple[datetime.datetime, datetime.datetime],
    ]
    lookup_name: str = ...
    def get_rhs_op(
        self, connection: DatabaseWrapper, rhs: Tuple[str, str]
    ) -> str: ...

class IsNull(BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Expression
    rhs: bool
    lookup_name: str = ...
    prepare_rhs: bool = ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...

class Regex(BuiltinLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: str
    lookup_name: str = ...
    prepare_rhs: bool = ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...

class IRegex(Regex):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.expressions.Col
    rhs: str
    lookup_name: str = ...

class YearLookup(Lookup):
    def year_lookup_bounds(
        self, connection: DatabaseWrapper, year: int
    ) -> List[str]: ...

class YearComparisonLookup(YearLookup):
    bilateral_transforms: List[Any]
    lhs: django.db.models.expressions.Value
    rhs: django.db.models.expressions.Value
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def get_bound(self, start: datetime, finish: datetime) -> Any: ...

class YearExact(YearLookup, Exact):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.functions.datetime.ExtractYear
    rhs: Union[django.db.models.functions.datetime.Extract, int, str]
    lookup_name: str = ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...

class YearGt(YearComparisonLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.functions.datetime.ExtractYear
    rhs: int
    lookup_name: str = ...
    def get_bound(self, start: str, finish: str) -> str: ...

class YearGte(YearComparisonLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.functions.datetime.ExtractYear
    rhs: int
    lookup_name: str = ...
    def get_bound(self, start: str, finish: str) -> str: ...

class YearLt(YearComparisonLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.functions.datetime.ExtractYear
    rhs: int
    lookup_name: str = ...
    def get_bound(self, start: str, finish: str) -> str: ...

class YearLte(YearComparisonLookup):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: django.db.models.functions.datetime.ExtractYear
    rhs: int
    lookup_name: str = ...
    def get_bound(self, start: str, finish: str) -> str: ...
