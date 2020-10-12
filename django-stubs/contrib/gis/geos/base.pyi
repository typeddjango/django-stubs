from django.contrib.gis.ptr import CPointerBase as CPointerBase
from typing import Any

class GEOSBase(CPointerBase):
    null_ptr_exception_class: Any = ...
