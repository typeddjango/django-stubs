from typing import Any, ClassVar

from django.contrib.gis.db.backends.base.models import SpatialRefSysMixin
from django.db import models
from typing_extensions import Self

class PostGISGeometryColumns(models.Model):
    f_table_catalog: models.CharField
    f_table_schema: models.CharField
    f_table_name: models.CharField
    f_geometry_column: models.CharField
    coord_dimension: models.IntegerField
    srid: models.IntegerField
    type: models.CharField
    objects: ClassVar[models.Manager[Self]]

    @classmethod
    def table_name_col(cls) -> Any: ...
    @classmethod
    def geom_col_name(cls) -> Any: ...

class PostGISSpatialRefSys(models.Model, SpatialRefSysMixin):
    srid: models.IntegerField
    auth_name: models.CharField
    auth_srid: models.IntegerField
    srtext: models.CharField
    proj4text: models.CharField
    objects: ClassVar[models.Manager[Self]]

    @property
    def wkt(self) -> Any: ...
