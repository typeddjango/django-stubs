from django.contrib.gis.db.backends.base.adapter import WKTAdapter as WKTAdapter
from typing import Any

class SpatiaLiteAdapter(WKTAdapter):
    def __conform__(self, protocol: Any): ...
