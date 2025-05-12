from django.contrib.gis.forms import (
    GeometryCollectionField,
    GeometryField,
    LineStringField,
    MultiLineStringField,
    MultiPointField,
    MultiPolygonField,
    PointField,
    PolygonField,
)
from django.contrib.gis.forms.widgets import OpenLayersWidget
from typing_extensions import assert_type

assert_type(GeometryField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(GeometryField().widget, OpenLayersWidget)

assert_type(GeometryCollectionField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(GeometryCollectionField().widget, OpenLayersWidget)

assert_type(PointField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(PointField().widget, OpenLayersWidget)

assert_type(MultiPointField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(MultiPointField().widget, OpenLayersWidget)

assert_type(LineStringField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(LineStringField().widget, OpenLayersWidget)

assert_type(MultiLineStringField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(MultiLineStringField().widget, OpenLayersWidget)

assert_type(PolygonField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(PolygonField().widget, OpenLayersWidget)

assert_type(MultiPolygonField.widget, type[OpenLayersWidget] | OpenLayersWidget)
assert_type(MultiPolygonField().widget, OpenLayersWidget)
