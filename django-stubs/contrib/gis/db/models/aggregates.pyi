from typing import Any

from django.db.models import Aggregate

class GeoAggregate(Aggregate):
    is_extent: bool
    def as_oracle(self, compiler: Any, connection: Any, **extra_context: Any) -> Any: ...

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
