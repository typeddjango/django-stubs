from collections.abc import Iterable
from typing import Any, NamedTuple, TypeVar

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
    description: Any
    form_class: Any
    geom_type: str
    geom_class: Any
    dim: Any
    geography: Any
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
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class LineStringField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class PolygonField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class MultiPointField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class MultiLineStringField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class MultiPolygonField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class GeometryCollectionField(GeometryField):
    geom_type: str
    geom_class: Any
    form_class: Any
    description: Any

class ExtentField(Field):
    description: Any
    def get_internal_type(self) -> Any: ...
    def select_format(self, compiler: Any, sql: Any, params: Any) -> Any: ...

class RasterField(BaseSpatialField):
    description: Any
    geom_type: str
    geography: bool
    def db_type(self, connection: Any) -> Any: ...
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any: ...
    def get_transform(self, name: Any) -> Any: ...
