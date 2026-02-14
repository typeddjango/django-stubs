from collections.abc import Callable

from django.http.response import HttpResponseBase
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from typing_extensions import assert_type

decorator = decorator_from_middleware(CacheMiddleware)  # pyrefly: ignore[bad-argument-type]
assert_type(
    decorator,
    Callable[[Callable[..., HttpResponseBase]], Callable[..., HttpResponseBase]],
)

factory = decorator_from_middleware_with_args(CacheMiddleware)  # pyrefly: ignore[bad-argument-type]
assert_type(
    factory,
    Callable[..., Callable[[Callable[..., HttpResponseBase]], Callable[..., HttpResponseBase]]],
)
