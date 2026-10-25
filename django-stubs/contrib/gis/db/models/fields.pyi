from collections.abc import Iterable
from typing import Any, Literal, NamedTuple, overload

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
from django.db.models import Model
from django.db.models.expressions import Expression
from django.db.models.fields import NOT_PROVIDED, Field, FieldInitKwargs, _ErrorMessagesMapping, _GT_co, _ST_contra
from django.db.models.sql.compiler import _AsSqlType
from django.forms.widgets import Widget
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar, Unpack, override

class SRIDCacheEntry(NamedTuple):
    units: Any
    units_name: str
    spheroid: str
    geodetic: bool

def get_srid_info(srid: int, connection: Any) -> SRIDCacheEntry: ...

class BaseSpatialField(Field[_ST_contra, _GT_co]):
    form_class: type[forms.GeometryField]
    geom_type: str
    geom_class: type[GEOSGeometry] | None
    geography: bool
    spatial_index: bool
    srid: int
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        srid: int = 4326,
        spatial_index: bool = True,
        *,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @override
    def db_type(self, connection: Any) -> Any: ...
    def spheroid(self, connection: Any) -> Any: ...
    def units(self, connection: Any) -> Any: ...
    def units_name(self, connection: Any) -> Any: ...
    def geodetic(self, connection: Any) -> Any: ...
    def get_placeholder_sql(self, value: Any, compiler: Any, connection: Any) -> _AsSqlType: ...
    def get_srid(self, obj: Any) -> Any: ...
    @override
    def get_db_prep_value(self, value: Any, connection: Any, *args: Any, **kwargs: Any) -> Any: ...
    def get_raster_prep_value(self, value: Any, is_candidate: Any) -> Any: ...
    @override
    def get_prep_value(self, value: Any) -> Any: ...

class GeometryField(BaseSpatialField[_ST_contra, _GT_co]):
    dim: int
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @override
    def contribute_to_class(self, cls: type[Model], name: str, **kwargs: Any) -> None: ...  # type: ignore[override]
    @override
    def formfield(  # type: ignore[override]
        self,
        *,
        form_class: type[forms.GeometryField] | None = ...,
        choices_form_class: type[forms.GeometryField] | None = ...,
        required: bool = ...,
        widget: Widget | type[Widget] | None = ...,
        label: _StrOrPromise | None = ...,
        initial: Any | None = ...,
        help_text: _StrOrPromise = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        show_hidden_initial: bool = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: str | None = ...,
        # GeometryField adds `geom_type` and `srid`
        geom_type: str = ...,
        srid: Any = ...,
        **kwargs: Any,
    ) -> forms.GeometryField | None: ...

_ST_Point_contra = TypeVar("_ST_Point_contra", contravariant=True, default=Point)
_GT_Point_co = TypeVar("_GT_Point_co", covariant=True, default=Point)

class PointField(GeometryField[_ST_Point_contra, _GT_Point_co]):
    _pyi_private_set_type: Point
    _pyi_private_get_type: Point
    _pyi_lookup_exact_type: Point
    @overload
    def __init__(
        self: PointField[Point | None, Point | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[Point]
    form_class: type[forms.PointField]

_ST_LineString_contra = TypeVar("_ST_LineString_contra", contravariant=True, default=LineString)
_GT_LineString_co = TypeVar("_GT_LineString_co", covariant=True, default=LineString)

class LineStringField(GeometryField[_ST_LineString_contra, _GT_LineString_co]):
    _pyi_private_set_type: LineString
    _pyi_private_get_type: LineString
    _pyi_lookup_exact_type: LineString
    @overload
    def __init__(
        self: LineStringField[LineString | None, LineString | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[LineString]
    form_class: type[forms.LineStringField]

_ST_Polygon_contra = TypeVar("_ST_Polygon_contra", contravariant=True, default=Polygon)
_GT_Polygon_co = TypeVar("_GT_Polygon_co", covariant=True, default=Polygon)

class PolygonField(GeometryField[_ST_Polygon_contra, _GT_Polygon_co]):
    _pyi_private_set_type: Polygon
    _pyi_private_get_type: Polygon
    _pyi_lookup_exact_type: Polygon
    @overload
    def __init__(
        self: PolygonField[Polygon | None, Polygon | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[Polygon]
    form_class: type[forms.PolygonField]

_ST_MultiPoint_contra = TypeVar("_ST_MultiPoint_contra", contravariant=True, default=MultiPoint)
_GT_MultiPoint_co = TypeVar("_GT_MultiPoint_co", covariant=True, default=MultiPoint)

class MultiPointField(GeometryField[_ST_MultiPoint_contra, _GT_MultiPoint_co]):
    _pyi_private_set_type: MultiPoint
    _pyi_private_get_type: MultiPoint
    _pyi_lookup_exact_type: MultiPoint
    @overload
    def __init__(
        self: MultiPointField[MultiPoint | None, MultiPoint | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[MultiPoint]
    form_class: type[forms.MultiPointField]

_ST_MultiLineString_contra = TypeVar("_ST_MultiLineString_contra", contravariant=True, default=MultiLineString)
_GT_MultiLineString_co = TypeVar("_GT_MultiLineString_co", covariant=True, default=MultiLineString)

class MultiLineStringField(GeometryField[_ST_MultiLineString_contra, _GT_MultiLineString_co]):
    _pyi_private_set_type: MultiLineString
    _pyi_private_get_type: MultiLineString
    _pyi_lookup_exact_type: MultiLineString
    @overload
    def __init__(
        self: MultiLineStringField[MultiLineString | None, MultiLineString | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[MultiLineString]
    form_class: type[forms.MultiLineStringField]

_ST_MultiPolygon_contra = TypeVar("_ST_MultiPolygon_contra", contravariant=True, default=MultiPolygon)
_GT_MultiPolygon_co = TypeVar("_GT_MultiPolygon_co", covariant=True, default=MultiPolygon)

class MultiPolygonField(GeometryField[_ST_MultiPolygon_contra, _GT_MultiPolygon_co]):
    _pyi_private_set_type: MultiPolygon
    _pyi_private_get_type: MultiPolygon
    _pyi_lookup_exact_type: MultiPolygon
    @overload
    def __init__(
        self: MultiPolygonField[MultiPolygon | None, MultiPolygon | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[MultiPolygon]
    form_class: type[forms.MultiPolygonField]

_ST_GeometryCollection_contra = TypeVar("_ST_GeometryCollection_contra", contravariant=True, default=GeometryCollection)
_GT_GeometryCollection_co = TypeVar("_GT_GeometryCollection_co", covariant=True, default=GeometryCollection)

class GeometryCollectionField(GeometryField[_ST_GeometryCollection_contra, _GT_GeometryCollection_co]):
    _pyi_private_set_type: GeometryCollection
    _pyi_private_get_type: GeometryCollection
    _pyi_lookup_exact_type: GeometryCollection
    @overload
    def __init__(
        self: GeometryCollectionField[GeometryCollection | None, GeometryCollection | None],
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        dim: int = 2,
        geography: bool = False,
        *,
        extent: tuple[float, float, float, float] = ...,
        tolerance: float = 0.05,
        max_geom_collections: int | None = ...,
        srid: int = 4326,
        spatial_index: bool = True,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...

    geom_class: type[GeometryCollection]
    form_class: type[forms.GeometryCollectionField]

class ExtentField(Field[Any, Any]):
    @override
    def get_internal_type(self) -> str: ...

class RasterField(BaseSpatialField[_ST_contra, _GT_co]):
    @override
    def db_type(self, connection: Any) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    @override
    def contribute_to_class(self, cls: type[Model], name: str, **kwargs: Any) -> None: ...  # type: ignore[override]
    @override
    def get_transform(self, name: Any) -> Any: ...
