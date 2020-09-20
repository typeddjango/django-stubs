from django.contrib.gis.ptr import CPointerBase as CPointerBase
from typing import Any

class GDALBase(CPointerBase):
    null_ptr_exception_class: Any = ...
