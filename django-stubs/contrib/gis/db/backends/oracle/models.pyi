from typing import Any, ClassVar

from django.contrib.gis.db import models
from django.contrib.gis.db.backends.base.models import SpatialRefSysMixin
from django.db.models.manager import Manager
from typing_extensions import Self

class OracleGeometryColumns(models.Model):
    table_name: models.CharField
    column_name: models.CharField
    srid: models.IntegerField
    objects: ClassVar[Manager[Self]]

    @classmethod
    def table_name_col(cls) -> Any: ...
    @classmethod
    def geom_col_name(cls) -> Any: ...

class OracleSpatialRefSys(models.Model, SpatialRefSysMixin):
    cs_name: models.CharField
    srid: models.IntegerField
    auth_srid: models.IntegerField
    auth_name: models.CharField
    wktext: models.TextField
    cs_bounds: models.PolygonField
    objects: ClassVar[Manager[Self]]

    @property
    def wkt(self) -> Any: ...
