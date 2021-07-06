from typing import Any

from django.contrib.gis.gdal.base import GDALBase as GDALBase

class GDALRasterBase(GDALBase):
    @property
    def metadata(self): ...
    @metadata.setter
    def metadata(self, value: Any) -> None: ...
