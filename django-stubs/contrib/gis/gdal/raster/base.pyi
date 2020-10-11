from django.contrib.gis.gdal.base import GDALBase as GDALBase
from typing import Any

class GDALRasterBase(GDALBase):
    @property
    def metadata(self): ...
    @metadata.setter
    def metadata(self, value: Any) -> None: ...
