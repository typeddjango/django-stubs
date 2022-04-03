from typing import Any, Type

from django.utils.connection import BaseConnectionHandler, ConnectionProxy

from .backends.base import BaseCache as BaseCache
from .backends.base import CacheKeyWarning as CacheKeyWarning
from .backends.base import InvalidCacheBackendError as InvalidCacheBackendError

DEFAULT_CACHE_ALIAS: str

class CacheHandler(BaseConnectionHandler):
    settings_name: str = ...
    exception_class: Type[Exception] = ...
    def create_connection(self, alias: str) -> BaseCache: ...
    def all(self, initialized_only: bool = ...): ...

def close_caches(**kwargs: Any) -> None: ...

cache: ConnectionProxy
caches: CacheHandler
