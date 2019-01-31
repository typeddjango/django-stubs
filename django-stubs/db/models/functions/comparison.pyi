from datetime import date
from decimal import Decimal
from typing import Any, Callable, Dict, List, Union

from django.db.models.expressions import Combinable, Expression

from django.db.models import Func
from django.db.models.fields import Field

class Cast(Func):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: Field
    source_expressions: List[Combinable]
    function: str = ...
    template: str = ...
    def __init__(self, expression: Union[date, Decimal, Expression, str], output_field: Union[str, Field]) -> None: ...

class Coalesce(Func):
    contains_aggregate: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: Field
    source_expressions: List[Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...

class Greatest(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: Field
    source_expressions: List[Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...

class Least(Func):
    contains_aggregate: bool
    contains_over_clause: bool
    convert_value: Callable
    extra: Dict[Any, Any]
    is_summary: bool
    output_field: Field
    source_expressions: List[Combinable]
    function: str = ...
    def __init__(self, *expressions: Any, **extra: Any) -> None: ...
