from types import ModuleType
from typing import Any, Dict, Sequence, Type, Union

from django.core.cache.backends.base import BaseCache

class BaseMemcachedCache(BaseCache):
    def __init__(
        self,
        server: Union[str, Sequence[str]],
        params: Dict[str, Any],
        library: ModuleType,
        value_not_found_exception: Type[BaseException],
    ) -> None: ...

class MemcachedCache(BaseMemcachedCache):
    def __init__(self, server: Union[str, Sequence[str]], params: Dict[str, Any]) -> None: ...

class PyLibMCCache(BaseMemcachedCache):
    def __init__(self, server: Union[str, Sequence[str]], params: Dict[str, Any]) -> None: ...
