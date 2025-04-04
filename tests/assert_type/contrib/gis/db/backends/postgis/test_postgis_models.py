from django.contrib.gis.db.backends.postgis.models import PostGISGeometryColumns, PostGISSpatialRefSys
from django.db.models.manager import Manager
from typing_extensions import assert_type

columns = PostGISGeometryColumns()
assert_type(columns.f_table_catalog, str)
assert_type(columns.f_table_schema, str)
assert_type(columns.f_table_name, str)
assert_type(columns.f_geometry_column, str)
assert_type(columns.coord_dimension, int)
assert_type(columns.srid, int)
assert_type(columns.type, str)
assert_type(columns.objects, Manager[PostGISGeometryColumns])

spatial_ref_sys = PostGISSpatialRefSys()
assert_type(spatial_ref_sys.srid, int)
assert_type(spatial_ref_sys.auth_name, str)
assert_type(spatial_ref_sys.auth_srid, int)
assert_type(spatial_ref_sys.srtext, str)
assert_type(spatial_ref_sys.proj4text, str)
assert_type(spatial_ref_sys.objects, Manager[PostGISSpatialRefSys])
