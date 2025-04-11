from typing import Any, ClassVar

from django.contrib.gis.db.backends.base.models import SpatialRefSysMixin
from django.db import models
from typing_extensions import Self

class SpatialiteGeometryColumns(models.Model):
    f_table_name: models.CharField
    f_geometry_column: models.CharField
    coord_dimension: models.IntegerField
    srid: models.IntegerField
    spatial_index_enabled: models.IntegerField
    type: models.IntegerField
    objects: ClassVar[models.Manager[Self]]

    @classmethod
    def table_name_col(cls) -> Any: ...
    @classmethod
    def geom_col_name(cls) -> Any: ...

class SpatialiteSpatialRefSys(models.Model, SpatialRefSysMixin):
    srid: models.IntegerField
    auth_name: models.CharField
    auth_srid: models.IntegerField
    ref_sys_name: models.CharField
    proj4text: models.CharField
    srtext: models.CharField
    objects: ClassVar[models.Manager[Self]]

    @property
    def wkt(self) -> Any: ...
