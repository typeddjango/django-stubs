from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.core.cache.backends.base import BaseCache
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse


class FileBasedCache(BaseCache):
    default_timeout: int
    key_func: Callable
    key_prefix: str
    version: int
    cache_suffix: str = ...
    def __init__(
        self,
        dir: str,
        params: Union[
            Dict[str, Callable],
            Dict[str, Dict[str, int]],
            Dict[str, int],
            Dict[str, str],
        ],
    ) -> None: ...
    def add(
        self,
        key: str,
        value: Union[Dict[str, int], bytes, int, str],
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> bool: ...
    def get(
        self,
        key: str,
        default: Optional[Union[int, str]] = ...,
        version: Optional[int] = ...,
    ) -> Optional[str]: ...
    def set(
        self,
        key: str,
        value: Union[
            Dict[
                str,
                Union[
                    Callable,
                    Dict[str, int],
                    List[int],
                    Tuple[int, int, int, int],
                    Type[Any],
                    int,
                    str,
                ],
            ],
            List[Any],
            bytes,
            Model,
            QuerySet,
            HttpResponse,
            int,
            str,
        ],
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> None: ...
    def touch(
        self, key: str, timeout: Any = ..., version: None = ...
    ) -> bool: ...
    def delete(self, key: str, version: Optional[int] = ...) -> None: ...
    def has_key(self, key: str, version: Optional[int] = ...) -> bool: ...
    def clear(self) -> None: ...
