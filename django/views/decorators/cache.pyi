from typing import (
    Callable,
    Union,
)


def cache_page(timeout: Union[float, int], *, cache = ..., key_prefix = ...) -> Callable: ...


def never_cache(view_func: Callable) -> Callable: ...