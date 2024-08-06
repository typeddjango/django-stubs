from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Aggregate, Expression
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType

class GeoAggregate(Aggregate):
    is_extent: bool
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, **extra_context: Any) -> _AsSqlType: ...

class Collect(GeoAggregate):
    name: str
    output_field_class: Any

class Extent(GeoAggregate):
    name: str
    def __init__(self, expression: Any, **extra: Any) -> None: ...
    def convert_value(self, value: Any, expression: Expression, connection: BaseDatabaseWrapper) -> Any: ...

class Extent3D(GeoAggregate):
    name: str
    def __init__(self, expression: Any, **extra: Any) -> None: ...
    def convert_value(self, value: Any, expression: Expression, connection: BaseDatabaseWrapper) -> Any: ...

class MakeLine(GeoAggregate):
    name: str
    output_field_class: Any

class Union(GeoAggregate):
    name: str
    output_field_class: Any
