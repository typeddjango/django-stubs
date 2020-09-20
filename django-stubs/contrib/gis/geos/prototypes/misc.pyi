from django.contrib.gis.geos.libgeos import GEOSFuncFactory
from typing import Any

class DblFromGeom(GEOSFuncFactory):
    restype: Any = ...
    errcheck: Any = ...

geos_area: Any
geos_distance: Any
geos_length: Any
geos_isvalidreason: Any
