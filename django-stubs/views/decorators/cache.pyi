from typing import Callable


def cache_page(timeout: float, *, cache = ..., key_prefix = ...) -> Callable: ...


def never_cache(view_func: Callable) -> Callable: ...