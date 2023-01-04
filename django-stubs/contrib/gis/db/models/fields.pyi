from collections.abc import Iterable
from typing import Any, NamedTuple, TypeVar

from django.contrib.gis import forms
from django.contrib.gis.geos import (
    GeometryCollection,
    GEOSGeometry,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from django.core.validators import _ValidatorCallable
from django.db.models.fields import Field, _ErrorMessagesT, _FieldChoices
from django.utils.functional import _StrOrPromise

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class SRIDCacheEntry(NamedTuple):
    units: Any
    units_name: str
    geodetic: bool
    spheroid: str

def get_srid_info(srid: int, connection: Any) -> SRIDCacheEntry: ...

class BaseSpatialField(Field[_ST, _GT]):
    form_class: type[forms.GeometryField]
    geom_type: str
    geom_class: type[GEOSGeometry] | None
    geography: bool
    spatial_index: bool
    srid: int
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        srid: int = ...,
        spatial_index: bool = ...,
        *,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _FieldChoices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesT | None = ...,
    ) -> None: ...
    def deconstruct(self) -> Any: ...
    def db_type(self, connection: Any) -> Any: ...
    def spheroid(self, connection: Any) -> Any: ...
    def units(self, connection: Any) -> Any: ...
    def units_name(self, connection: Any) -> Any: ...
    def geodetic(self, connection: Any) -> Any: ...
    def get_placeholder(self, value: Any, compiler: Any, connection: Any) -> Any: ...
    def get_srid(self, obj: Any) -> Any: ...
    def get_db_prep_value(self, value: Any, connection: Any, *args: Any, **kwargs: Any) -> Any: ...
    def get_raster_prep_value(self, value: Any, is_candidate: Any) -> Any: ...
    def get_prep_value(self, value: Any) -> Any: ...

class GeometryField(BaseSpatialField):
    dim: int
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        dim: int = ...,
        geography: bool = ...,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = ...,
        srid: int = ...,
        spatial_index: bool = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _FieldChoices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesT | None = ...,
    ) -> None: ...
    def deconstruct(self) -> Any: ...
    def formfield(self, **kwargs: Any) -> Any: ...  # type: ignore[override]
    def select_format(self, compiler: Any, sql: Any, params: Any) -> Any: ...

class PointField(GeometryField):
    geom_class: type[Point]
    form_class: type[forms.PointField]

class LineStringField(GeometryField):
    geom_class: type[LineString]
    form_class: type[forms.LineStringField]

class PolygonField(GeometryField):
    geom_class: type[Polygon]
    form_class: type[forms.PolygonField]

class MultiPointField(GeometryField):
    geom_class: type[MultiPoint]
    form_class: type[forms.MultiPointField]

class MultiLineStringField(GeometryField):
    geom_class: type[MultiLineString]
    form_class: type[forms.MultiLineStringField]

class MultiPolygonField(GeometryField):
    geom_class: type[MultiPolygon]
    form_class: type[forms.MultiPolygonField]

class GeometryCollectionField(GeometryField):
    geom_class: type[GeometryCollection]
    form_class: type[forms.GeometryCollectionField]

class ExtentField(Field):
    def get_internal_type(self) -> Any: ...
    def select_format(self, compiler: Any, sql: Any, params: Any) -> Any: ...

class RasterField(BaseSpatialField):
    def db_type(self, connection: Any) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def get_transform(self, name: Any) -> Any: ...
