from typing import Any

from django.core.cache.backends.base import BaseCache

class LocMemCache(BaseCache):
    def __init__(self, name: str, params: dict[str, Any]) -> None: ...
