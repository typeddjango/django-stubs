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
from django.forms.widgets import Widget
from typing_extensions import assert_type

assert_type(GeometryField.widget, type[Widget] | Widget)
assert_type(GeometryField().widget, Widget)

assert_type(GeometryCollectionField.widget, type[Widget] | Widget)
assert_type(GeometryCollectionField().widget, Widget)

assert_type(PointField.widget, type[Widget] | Widget)
assert_type(PointField().widget, Widget)

assert_type(MultiPointField.widget, type[Widget] | Widget)
assert_type(MultiPointField().widget, Widget)

assert_type(LineStringField.widget, type[Widget] | Widget)
assert_type(LineStringField().widget, Widget)

assert_type(MultiLineStringField.widget, type[Widget] | Widget)
assert_type(MultiLineStringField().widget, Widget)

assert_type(PolygonField.widget, type[Widget] | Widget)
assert_type(PolygonField().widget, Widget)

assert_type(MultiPolygonField.widget, type[Widget] | Widget)
assert_type(MultiPolygonField().widget, Widget)
