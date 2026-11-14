from typing import Any

from django.contrib.gis.measure import Area, Distance
from django.db import models
from typing_extensions import TypeVar, override

# __set__ value type
_ST_contra = TypeVar("_ST_contra", contravariant=True, default=Any)
# __get__ return type
_GT_co = TypeVar("_GT_co", covariant=True, default=Any)

class AreaField(models.FloatField[_ST_contra, _GT_co]):
    _pyi_private_get_type: Area  # type: ignore[assignment]
    geo_field: Any
    def __init__(self, geo_field: Any) -> None: ...
    @override
    def get_prep_value(self, value: Any) -> Any: ...
    @override
    def get_db_prep_value(self, value: Any, connection: Any, prepared: bool = ...) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    @override
    def get_internal_type(self) -> Any: ...

class DistanceField(models.FloatField[_ST_contra, _GT_co]):
    _pyi_private_get_type: Distance  # type: ignore[assignment]
    geo_field: Any
    def __init__(self, geo_field: Any) -> None: ...
    @override
    def get_prep_value(self, value: Any) -> Any: ...
    @override
    def get_db_prep_value(self, value: Any, connection: Any, prepared: bool = ...) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    @override
    def get_internal_type(self) -> Any: ...
