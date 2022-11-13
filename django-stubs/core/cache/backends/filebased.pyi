from typing import Any

from django.core.cache.backends.base import BaseCache

class FileBasedCache(BaseCache):
    cache_suffix: str
    def __init__(self, dir: str, params: dict[str, Any]) -> None: ...
