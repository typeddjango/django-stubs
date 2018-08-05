from datetime import datetime
from typing import Any, Callable, Dict, Optional, Union

from django.core.cache.backends.base import BaseCache


class LocMemCache(BaseCache):
    default_timeout: int
    key_func: Callable
    key_prefix: str
    version: int
    def __init__(
        self,
        name: str,
        params: Dict[str, Optional[Union[Dict[str, int], Callable, str, int]]],
    ) -> None: ...
    def add(
        self,
        key: str,
        value: Union[
            Dict[str, Union[str, datetime]], int, bytes, str, Dict[str, int]
        ],
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> Any: ...
    def get(
        self,
        key: Union[str, int],
        default: Optional[Union[str, int]] = ...,
        version: Optional[int] = ...,
    ) -> Any: ...
    def set(
        self,
        key: Union[str, int],
        value: Any,
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> None: ...
    def touch(
        self, key: str, timeout: Any = ..., version: None = ...
    ) -> Any: ...
    def incr(
        self,
        key: Union[str, int],
        delta: int = ...,
        version: Optional[int] = ...,
    ) -> int: ...
    def has_key(self, key: str, version: Optional[int] = ...) -> Any: ...
    def delete(self, key: str, version: Optional[int] = ...) -> None: ...
    def clear(self) -> None: ...
