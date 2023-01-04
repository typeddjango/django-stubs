from typing import Any

from django.contrib.admin import ModelAdmin
from django.contrib.gis.forms import BaseGeometryWidget

spherical_mercator_srid: int

class GISModelAdmin(ModelAdmin):
    gis_widget: BaseGeometryWidget
    gis_widget_kwargs: dict[str, Any]

class GeoModelAdmin(ModelAdmin):
    default_lon: int
    default_lat: int
    default_zoom: int
    display_wkt: bool
    display_srid: bool
    extra_js: Any
    num_zoom: int
    max_zoom: bool
    min_zoom: bool
    units: str | bool
    max_resolution: str | bool
    max_extent: str | bool
    modifiable: bool
    mouse_position: bool
    scale_text: bool
    layerswitcher: bool
    scrollable: bool
    map_width: int
    map_height: int
    map_srid: int
    map_template: str
    openlayers_url: str
    point_zoom: Any
    wms_url: str
    wms_layer: str
    wms_name: str
    wms_options: Any
    debug: bool
    widget: Any
    @property
    def media(self) -> Any: ...
    def get_map_widget(self, db_field: Any) -> Any: ...

class OSMGeoAdmin(GeoModelAdmin):
    map_template: str
    num_zoom: int
    map_srid: Any
    max_extent: str
    max_resolution: str
    point_zoom: int
    units: str
