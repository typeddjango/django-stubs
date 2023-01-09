from collections.abc import Sequence
from types import ModuleType
from typing import Any

from django.core.cache.backends.base import BaseCache

class BaseMemcachedCache(BaseCache):
    def __init__(
        self,
        server: str | Sequence[str],
        params: dict[str, Any],
        library: ModuleType,
        value_not_found_exception: type[BaseException],
    ) -> None: ...

class MemcachedCache(BaseMemcachedCache):
    def __init__(self, server: str | Sequence[str], params: dict[str, Any]) -> None: ...

class PyLibMCCache(BaseMemcachedCache):
    def __init__(self, server: str | Sequence[str], params: dict[str, Any]) -> None: ...

class PyMemcacheCache(BaseMemcachedCache):
    def __init__(self, server: str | Sequence[str], params: dict[str, Any]) -> None: ...
