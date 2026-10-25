from __future__ import annotations

from typing import assert_type

from django.contrib.gis.db.models import fields
from django.contrib.gis.geos import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from django.db import models


class Geo(models.Model):
    point = fields.PointField()
    line_string = fields.LineStringField()
    polygon = fields.PolygonField()
    multi_point = fields.MultiPointField()
    multi_line_string = fields.MultiLineStringField()
    multi_polygon = fields.MultiPolygonField()
    geometry_collection = fields.GeometryCollectionField()
    null_point = fields.PointField(null=True)
    null_line_string = fields.LineStringField(null=True)
    null_polygon = fields.PolygonField(null=True)
    null_multi_point = fields.MultiPointField(null=True)
    null_multi_line_string = fields.MultiLineStringField(null=True)
    null_multi_polygon = fields.MultiPolygonField(null=True)
    null_geometry_collection = fields.GeometryCollectionField(null=True)


def fields_getter_and_setter() -> None:
    geo = Geo()
    assert_type(geo.point, Point)
    geo.point = Point()
    assert_type(geo.line_string, LineString)
    geo.line_string = LineString()
    assert_type(geo.polygon, Polygon)
    geo.polygon = Polygon()
    assert_type(geo.multi_point, MultiPoint)
    geo.multi_point = MultiPoint()
    assert_type(geo.multi_line_string, MultiLineString)
    geo.multi_line_string = MultiLineString()
    assert_type(geo.multi_polygon, MultiPolygon)
    geo.multi_polygon = MultiPolygon()
    assert_type(geo.geometry_collection, GeometryCollection)
    geo.geometry_collection = GeometryCollection()


def nullable_geometry_fields_read_optional() -> None:
    geo = Geo()
    assert_type(geo.null_point, Point | None)
    assert_type(geo.null_line_string, LineString | None)
    assert_type(geo.null_polygon, Polygon | None)
    assert_type(geo.null_multi_point, MultiPoint | None)
    assert_type(geo.null_multi_line_string, MultiLineString | None)
    assert_type(geo.null_multi_polygon, MultiPolygon | None)
    assert_type(geo.null_geometry_collection, GeometryCollection | None)
    geo.null_point = None
    geo.point = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]
