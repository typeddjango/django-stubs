from django.contrib.gis.db.backends.spatialite.models import SpatialiteGeometryColumns, SpatialiteSpatialRefSys
from django.db.models.manager import Manager
from typing_extensions import assert_type

columns = SpatialiteGeometryColumns()
assert_type(columns.f_table_name, str)
assert_type(columns.f_geometry_column, str)
assert_type(columns.coord_dimension, int)
assert_type(columns.srid, int)
assert_type(columns.spatial_index_enabled, int)
assert_type(columns.type, int)
assert_type(columns.objects, Manager[SpatialiteGeometryColumns])

spatial_ref_sys = SpatialiteSpatialRefSys()
assert_type(spatial_ref_sys.srid, int)
assert_type(spatial_ref_sys.auth_name, str)
assert_type(spatial_ref_sys.auth_srid, int)
assert_type(spatial_ref_sys.ref_sys_name, str)
assert_type(spatial_ref_sys.proj4text, str)
assert_type(spatial_ref_sys.srtext, str)
assert_type(spatial_ref_sys.objects, Manager[SpatialiteSpatialRefSys])
