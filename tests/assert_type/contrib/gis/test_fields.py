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
    assert_type(geo.point, Point)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.point = Point()
    assert_type(geo.line_string, LineString)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.line_string = LineString()
    assert_type(geo.polygon, Polygon)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.polygon = Polygon()
    assert_type(geo.multi_point, MultiPoint)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.multi_point = MultiPoint()
    assert_type(geo.multi_line_string, MultiLineString)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.multi_line_string = MultiLineString()
    assert_type(geo.multi_polygon, MultiPolygon)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.multi_polygon = MultiPolygon()
    assert_type(geo.geometry_collection, GeometryCollection)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.geometry_collection = GeometryCollection()


def nullable_geometry_fields_read_optional() -> None:
    geo = Geo()
    assert_type(geo.null_point, Point | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_line_string, LineString | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_polygon, Polygon | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_multi_point, MultiPoint | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_multi_line_string, MultiLineString | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_multi_polygon, MultiPolygon | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(geo.null_geometry_collection, GeometryCollection | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    geo.null_point = None
    geo.point = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]
