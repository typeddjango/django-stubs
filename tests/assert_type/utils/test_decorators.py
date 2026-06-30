from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBase
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import (
    classonlymethod,
    decorator_from_middleware,
    decorator_from_middleware_with_args,
    method_decorator,
)
from django.views.generic.base import View
from typing_extensions import assert_type, override

if TYPE_CHECKING:
    from django.http.request import HttpRequest

decorator = decorator_from_middleware(CacheMiddleware)
assert_type(
    decorator,
    Callable[[Callable[..., HttpResponseBase]], Callable[..., HttpResponseBase]],
)

factory = decorator_from_middleware_with_args(CacheMiddleware)
assert_type(
    factory,
    Callable[..., Callable[[Callable[..., HttpResponseBase]], Callable[..., HttpResponseBase]]],
)


# classonlymethod
class Bananaman:
    @classonlymethod
    def count_bananas(cls) -> int:
        return 12


assert_type(Bananaman.count_bananas(), int)


# method_decorator on class
@method_decorator(login_required, name="dispatch")
class DecoratedView(View): ...


assert_type(DecoratedView(), DecoratedView)


# method_decorator on function
class TestView(View):
    @method_decorator(login_required)
    @override
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        return super().dispatch(request, *args, **kwargs)
