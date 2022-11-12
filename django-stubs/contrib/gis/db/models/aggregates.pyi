from typing import Any

from django.db.models import Aggregate
from django.db.models.sql.compiler import _AsSqlType

class GeoAggregate(Aggregate):
    function: Any
    is_extent: bool
    @property
    def output_field(self) -> Any: ...
    def as_sql(
        self, compiler: Any, connection: Any, function: Any | None = ..., **extra_context: Any
    ) -> _AsSqlType: ...
    def as_oracle(self, compiler: Any, connection: Any, **extra_context: Any) -> Any: ...
    def resolve_expression(
        self,
        query: Any | None = ...,
        allow_joins: bool = ...,
        reuse: Any | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> Any: ...

class Collect(GeoAggregate):
    name: str
    output_field_class: Any

class Extent(GeoAggregate):
    name: str
    def __init__(self, expression: Any, **extra: Any) -> None: ...

class Extent3D(GeoAggregate):
    name: str
    def __init__(self, expression: Any, **extra: Any) -> None: ...

class MakeLine(GeoAggregate):
    name: str
    output_field_class: Any

class Union(GeoAggregate):
    name: str
    output_field_class: Any
