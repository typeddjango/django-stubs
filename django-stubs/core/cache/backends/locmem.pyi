from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.core.cache.backends.base import BaseCache
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse


class LocMemCache(BaseCache):
    default_timeout: int
    key_func: Callable
    key_prefix: str
    version: int
    def __init__(
        self,
        name: str,
        params: Union[
            Dict[str, Callable],
            Dict[str, Dict[str, int]],
            Dict[str, None],
            Dict[str, int],
            Dict[str, str],
        ],
    ) -> None: ...
    def add(
        self,
        key: str,
        value: Union[
            Dict[str, Union[datetime, str]], Dict[str, int], bytes, int, str
        ],
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> Any: ...
    def get(
        self,
        key: Union[int, str],
        default: Optional[Union[int, str]] = ...,
        version: Optional[int] = ...,
    ) -> Union[
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
        List[str],
        bytes,
        Model,
        QuerySet,
        HttpResponse,
        int,
        str,
    ]: ...
    def set(
        self,
        key: Union[int, str],
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
            Dict[str, Union[datetime, str]],
            List[str],
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
    ) -> Any: ...
    def incr(
        self,
        key: Union[int, str],
        delta: int = ...,
        version: Optional[int] = ...,
    ) -> int: ...
    def has_key(self, key: str, version: Optional[int] = ...) -> Any: ...
    def delete(self, key: str, version: Optional[int] = ...) -> None: ...
    def clear(self) -> None: ...
