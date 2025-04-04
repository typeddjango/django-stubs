from django.contrib.gis.db.backends.oracle.models import OracleGeometryColumns, OracleSpatialRefSys
from django.contrib.gis.geos.polygon import Polygon
from django.db.models.manager import Manager
from typing_extensions import assert_type

columns = OracleGeometryColumns()
assert_type(columns.table_name, str)
assert_type(columns.column_name, str)
assert_type(columns.srid, int)
assert_type(columns.objects, Manager[OracleGeometryColumns])

spatial_ref_sys = OracleSpatialRefSys()
assert_type(spatial_ref_sys.cs_name, str)
assert_type(spatial_ref_sys.srid, int)
assert_type(spatial_ref_sys.auth_srid, int)
assert_type(spatial_ref_sys.auth_name, str)
assert_type(spatial_ref_sys.wktext, str)
assert_type(spatial_ref_sys.cs_bounds, Polygon)
assert_type(spatial_ref_sys.objects, Manager[OracleSpatialRefSys])
