from typing import Callable


def vary_on_cookie(func: Callable) -> Callable: ...


def vary_on_headers(*headers) -> Callable: ...