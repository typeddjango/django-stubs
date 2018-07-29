from collections import OrderedDict
from datetime import datetime
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import (
    Col,
    CombinedExpression,
    Expression,
    Ref,
)
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.utils.datastructures import OrderedSet
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


class BuiltinLookup:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def process_lhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        lhs: Optional[Col] = ...
    ) -> Union[Tuple[str, List[str]], Tuple[str, List[int]], Tuple[str, List[Union[str, int]]], Tuple[str, List[Any]]]: ...


class Exact:
    def process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...


class FieldGetDbPrepValueIterableMixin:
    def batch_process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        rhs: Optional[OrderedSet] = ...
    ) -> Any: ...
    def get_prep_lookup(self) -> Any: ...
    def process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...
    def resolve_expression_parameter(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        sql: str,
        param: Any
    ) -> Union[Tuple[str, List[None]], Tuple[str, List[int]], Tuple[str, List[Any]], Tuple[str, List[str]]]: ...


class FieldGetDbPrepValueMixin:
    def get_db_prep_lookup(self, value: Any, connection: DatabaseWrapper) -> Any: ...


class IExact:
    def process_rhs(
        self,
        qn: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[Any]], Tuple[str, List[str]]]: ...


class In:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...


class IntegerFieldFloatRounding:
    def get_prep_lookup(
        self
    ) -> Union[Query, int, CombinedExpression]: ...


class IsNull:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...


class Lookup:
    def __init__(self, lhs: Any, rhs: Any) -> None: ...
    def apply_bilateral_transforms(
        self,
        value: Expression
    ) -> Transform: ...
    def batch_process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        rhs: Optional[OrderedSet] = ...
    ) -> Any: ...
    @cached_property
    def contains_aggregate(self) -> bool: ...
    @cached_property
    def contains_over_clause(self) -> bool: ...
    def get_db_prep_lookup(
        self,
        value: Union[str, int],
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[int]], Tuple[str, List[SafeText]], Tuple[str, List[str]]]: ...
    def get_group_by_cols(
        self
    ) -> Union[List[Col], List[CombinedExpression]]: ...
    def get_prep_lookup(self) -> Any: ...
    def get_source_expressions(self) -> List[Col]: ...
    def process_lhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper,
        lhs: Optional[Col] = ...
    ) -> Any: ...
    def process_rhs(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Any: ...
    def relabeled_clone(
        self,
        relabels: Union[OrderedDict, Dict[str, str], Dict[Union[str, None], str]]
    ) -> BuiltinLookup: ...
    def rhs_is_direct_value(self) -> bool: ...
    def set_source_expressions(self, new_exprs: List[Ref]) -> None: ...


class PatternLookup:
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...
    def process_rhs(
        self,
        qn: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[str]], Tuple[str, List[int]], Tuple[str, List[Any]]]: ...


class Range:
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: Tuple[str, str]) -> str: ...


class Regex:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...


class Transform:
    def get_bilateral_transforms(self) -> List[Type[Transform]]: ...
    @property
    def lhs(self) -> Expression: ...


class YearComparisonLookup:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Tuple[str, List[str]]: ...
    def get_bound(self, start: datetime, finish: datetime): ...
    def get_rhs_op(self, connection: DatabaseWrapper, rhs: str) -> str: ...


class YearExact:
    def as_sql(
        self,
        compiler: SQLCompiler,
        connection: DatabaseWrapper
    ) -> Union[Tuple[str, List[Any]], Tuple[str, List[str]]]: ...


class YearGt:
    def get_bound(self, start: str, finish: str) -> str: ...


class YearGte:
    def get_bound(self, start: str, finish: str) -> str: ...


class YearLookup:
    def year_lookup_bounds(self, connection: DatabaseWrapper, year: int) -> List[str]: ...


class YearLt:
    def get_bound(self, start: str, finish: str) -> str: ...


class YearLte:
    def get_bound(self, start: str, finish: str) -> str: ...