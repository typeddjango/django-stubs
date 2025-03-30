from collections.abc import Iterable
from typing import Any, Generic, NamedTuple, TypeVar, type_check_only

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
from django.db.models.expressions import Combinable, Expression
from django.db.models.fields import NOT_PROVIDED, Field, _ErrorMessagesMapping
from django.utils.choices import _Choices
from django.utils.functional import _StrOrPromise

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

_ST_PointField = TypeVar("_ST_PointField", default=Point | Combinable)
_GT_PointField = TypeVar("_GT_PointField", default=Point)
_Form_PointField = TypeVar("_Form_PointField", bound=forms.PointField, default=forms.PointField)
_Geom_PointField = TypeVar("_Geom_PointField", bound=Point, default=Point)

_ST_LineStringField = TypeVar("_ST_LineStringField", default=LineString | Combinable)
_GT_LineStringField = TypeVar("_GT_LineStringField", default=LineString)
_Form_LineStringField = TypeVar("_Form_LineStringField", bound=forms.LineStringField, default=forms.LineStringField)
_Geom_LineStringField = TypeVar("_Geom_LineStringField", bound=LineString, default=LineString)

_ST_PolygonField = TypeVar("_ST_PolygonField", default=Polygon | Combinable)
_GT_PolygonField = TypeVar("_GT_PolygonField", default=Polygon)
_Form_PolygonField = TypeVar("_Form_PolygonField", bound=forms.PolygonField, default=forms.PolygonField)
_Geom_PolygonField = TypeVar("_Geom_PolygonField", bound=Polygon, default=Polygon)

_ST_MultiPointField = TypeVar("_ST_MultiPointField", default=MultiPoint | Combinable)
_GT_MultiPointField = TypeVar("_GT_MultiPointField", default=MultiPoint)
_Form_MultiPointField = TypeVar("_Form_MultiPointField", bound=forms.MultiPointField, default=forms.MultiPointField)
_Geom_MultiPointField = TypeVar("_Geom_MultiPointField", bound=MultiPoint, default=MultiPoint)

_ST_MultiLineStringField = TypeVar("_ST_MultiLineStringField", default=MultiLineString | Combinable)
_GT_MultiLineStringField = TypeVar("_GT_MultiLineStringField", default=MultiLineString)
_Form_MultiLineStringField = TypeVar(
    "_Form_MultiLineStringField", bound=forms.MultiLineStringField, default=forms.MultiLineStringField
)
_Geom_MultiLineStringField = TypeVar("_Geom_MultiLineStringField", bound=MultiLineString, default=MultiLineString)

_ST_MultiPolygonField = TypeVar("_ST_MultiPolygonField", default=MultiPolygon | Combinable)
_GT_MultiPolygonField = TypeVar("_GT_MultiPolygonField", default=MultiPolygon)
_Form_MultiPolygonField = TypeVar(
    "_Form_MultiPolygonField", bound=forms.MultiPolygonField, default=forms.MultiPolygonField
)
_Geom_MultiPolygonField = TypeVar("_Geom_MultiPolygonField", bound=MultiPolygon, default=MultiPolygon)

_ST_GeometryCollectionField = TypeVar("_ST_GeometryCollectionField", default=GeometryCollection | Combinable)
_GT_GeometryCollectionField = TypeVar("_GT_GeometryCollectionField", default=GeometryCollection)
_Form_GeometryCollectionField = TypeVar(
    "_Form_GeometryCollectionField", bound=forms.GeometryCollectionField, default=forms.GeometryCollectionField
)
_Geom_GeometryCollectionField = TypeVar(
    "_Geom_GeometryCollectionField", bound=GeometryCollection, default=GeometryCollection
)

_Form_ClassT = TypeVar("_Form_ClassT", bound=forms.GeometryField)
_GEOM_ClassT = TypeVar("_GEOM_ClassT", bound=GEOSGeometry)

class SRIDCacheEntry(NamedTuple):
    units: Any
    units_name: str
    spheroid: str
    geodetic: bool

def get_srid_info(srid: int, connection: Any) -> SRIDCacheEntry: ...
@type_check_only
class SpatialClassField(Generic[_Form_ClassT, _GEOM_ClassT]):
    form_class: type[_Form_ClassT]
    geom_class: type[_GEOM_ClassT] | None

class BaseSpatialField(Field[_ST, _GT], SpatialClassField[_Form_ClassT, _GEOM_ClassT]):
    geom_type: str
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
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _Choices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
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

class GeometryField(BaseSpatialField[_ST, _GT, _Form_ClassT, _GEOM_ClassT]):
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
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _Choices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    def formfield(  # type: ignore[override]
        self,
        *,
        form_class: type[forms.GeometryField] | None = ...,
        geom_type: str = ...,
        srid: Any = ...,
        **kwargs: Any,
    ) -> forms.GeometryField: ...

class PointField(GeometryField[_ST_PointField, _GT_PointField, _Form_PointField, _Geom_PointField]):
    _pyi_private_set_type: Point | Combinable
    _pyi_private_get_type: Point
    _pyi_lookup_exact_type: Point

class LineStringField(
    GeometryField[_ST_LineStringField, _GT_LineStringField, _Form_LineStringField, _Geom_LineStringField]
):
    _pyi_private_set_type: LineString | Combinable
    _pyi_private_get_type: LineString
    _pyi_lookup_exact_type: LineString

class PolygonField(GeometryField[_ST_PolygonField, _GT_PolygonField, _Form_PolygonField, _Geom_PolygonField]):
    _pyi_private_set_type: Polygon | Combinable
    _pyi_private_get_type: Polygon
    _pyi_lookup_exact_type: Polygon

class MultiPointField(
    GeometryField[_ST_MultiPointField, _GT_MultiPointField, _Form_MultiPointField, _Geom_MultiPointField]
):
    _pyi_private_set_type: MultiPoint | Combinable
    _pyi_private_get_type: MultiPoint
    _pyi_lookup_exact_type: MultiPoint

class MultiLineStringField(
    GeometryField[
        _ST_MultiLineStringField, _GT_MultiLineStringField, _Form_MultiLineStringField, _Geom_MultiLineStringField
    ]
):
    _pyi_private_set_type: MultiLineString | Combinable
    _pyi_private_get_type: MultiLineString
    _pyi_lookup_exact_type: MultiLineString

class MultiPolygonField(
    GeometryField[_ST_MultiPolygonField, _GT_MultiPolygonField, _Form_MultiPolygonField, _Geom_MultiPolygonField]
):
    _pyi_private_set_type: MultiPolygon | Combinable
    _pyi_private_get_type: MultiPolygon
    _pyi_lookup_exact_type: MultiPolygon

class GeometryCollectionField(
    GeometryField[
        _ST_GeometryCollectionField,
        _GT_GeometryCollectionField,
        _Form_GeometryCollectionField,
        _Geom_GeometryCollectionField,
    ]
):
    _pyi_private_set_type: GeometryCollection | Combinable
    _pyi_private_get_type: GeometryCollection
    _pyi_lookup_exact_type: GeometryCollection

class ExtentField(Field):
    def get_internal_type(self) -> Any: ...

class RasterField(BaseSpatialField):
    def db_type(self, connection: Any) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def get_transform(self, name: Any) -> Any: ...
