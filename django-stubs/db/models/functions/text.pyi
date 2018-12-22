from typing import Any, List, Optional, Tuple, Union, Callable

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import Combinable, Expression, Value
from django.db.models.sql.compiler import SQLCompiler

from django.db.models import Func, Transform
from django.db.models.fields import Field

class BytesToCharFieldConversionMixin:
    def convert_value(
        self, value: str, expression: BytesToCharFieldConversionMixin, connection: DatabaseWrapper
    ) -> str: ...

class Chr(Transform):
    contains_aggregate: bool
    lookup_name: str = ...

class ConcatPair(Func):
    contains_aggregate: bool
    def coalesce(self) -> ConcatPair: ...

class Concat(Func):
    contains_aggregate: bool
    convert_value: Callable

class Left(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    output_field: Field
    def __init__(self, expression: str, length: Union[Value, int], **extra: Any) -> None: ...
    def get_substr(self) -> Substr: ...
    def use_substr(
        self, compiler: SQLCompiler, connection: DatabaseWrapper, **extra_context: Any
    ) -> Tuple[str, List[int]]: ...
    as_oracle: Any = ...
    as_sqlite: Any = ...

class Length(Transform):
    contains_aggregate: bool
    convert_value: Callable
    lookup_name: str = ...

class Lower(Transform):
    contains_aggregate: bool
    contains_column_references: bool
    contains_over_clause: bool
    convert_value: Callable
    lookup_name: str = ...

class LPad(BytesToCharFieldConversionMixin, Func):
    contains_aggregate: bool
    convert_value: Callable
    def __init__(self, expression: str, length: Union[Length, int], fill_text: Value = ..., **extra: Any) -> None: ...

class LTrim(Transform):
    contains_aggregate: bool
    convert_value: Callable
    lookup_name: str = ...

class Ord(Transform):
    contains_aggregate: bool
    convert_value: Callable
    lookup_name: str = ...
    def as_mysql(self, compiler: Any, connection: Any, **extra_context: Any): ...

class Repeat(BytesToCharFieldConversionMixin, Func):
    contains_aggregate: bool
    convert_value: Callable
    output_field: django.db.models.fields.CharField
    def __init__(self, expression: Union[Value, str], number: Union[Length, int], **extra: Any) -> None: ...
    def as_oracle(self, compiler: Any, connection: Any, **extra_context: Any): ...

class Replace(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    output_field: Field
    def __init__(self, expression: Combinable, text: Value, replacement: Value = ..., **extra: Any) -> None: ...

class Right(Left): ...

class RPad(LPad):
    output_field: Field

class RTrim(Transform):
    contains_aggregate: bool
    convert_value: Callable
    lookup_name: str = ...

class StrIndex(Func):
    contains_aggregate: bool
    convert_value: Callable
    output_field: Any = ...
    def as_postgresql(self, compiler: Any, connection: Any): ...

class Substr(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    output_field: Field
    def __init__(
        self,
        expression: Union[Expression, str],
        pos: Union[Expression, int],
        length: Optional[Union[Value, int]] = ...,
        **extra: Any
    ) -> None: ...

class Trim(Transform):
    contains_aggregate: bool
    convert_value: Callable
    lookup_name: str = ...

class Upper(Transform):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    lookup_name: str = ...
