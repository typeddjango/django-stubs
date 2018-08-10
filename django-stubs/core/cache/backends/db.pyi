from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.core.cache.backends.base import BaseCache
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponse


class Options:
    db_table: str = ...
    app_label: str = ...
    model_name: str = ...
    verbose_name: str = ...
    verbose_name_plural: str = ...
    object_name: str = ...
    abstract: bool = ...
    managed: bool = ...
    proxy: bool = ...
    swapped: bool = ...
    def __init__(self, table: str) -> None: ...

class BaseDatabaseCache(BaseCache):
    default_timeout: int
    key_func: Callable
    key_prefix: str
    version: int
    cache_model_class: Any = ...
    def __init__(
        self,
        table: str,
        params: Union[
            Dict[str, Callable],
            Dict[str, Dict[str, int]],
            Dict[str, int],
            Dict[str, str],
        ],
    ) -> None: ...

class DatabaseCache(BaseDatabaseCache):
    default_timeout: int
    key_func: Callable
    key_prefix: str
    version: int
    def get(
        self,
        key: str,
        default: Optional[Union[int, str]] = ...,
        version: Optional[int] = ...,
    ) -> Optional[
        Union[
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
        ]
    ]: ...
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
    def add(
        self,
        key: str,
        value: Union[Dict[str, int], bytes, int, str],
        timeout: Any = ...,
        version: Optional[int] = ...,
    ) -> bool: ...
    def touch(
        self, key: str, timeout: Any = ..., version: None = ...
    ) -> bool: ...
    def delete(self, key: str, version: Optional[int] = ...) -> None: ...
    def has_key(self, key: str, version: Optional[int] = ...) -> Any: ...
    def clear(self) -> None: ...
