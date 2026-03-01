from typing import Callable

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_protect
from typing_extensions import assert_type


@csrf_protect
def good_view_positional(request: HttpRequest, /) -> HttpResponse:
    return HttpResponse()


# `assert_type` can only be used when `request` is pos. only.
assert_type(good_view_positional, Callable[[HttpRequest], HttpResponse])


# The decorator works too if `request` is not explicitly pos. only.
@csrf_protect
def good_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


@csrf_protect
async def good_async_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse()


@csrf_protect
def good_view_with_arguments(request: HttpRequest, other: int, args: str) -> HttpResponse:
    return HttpResponse()


@csrf_protect
async def good_async_view_with_arguments(request: HttpRequest, other: int, args: str) -> HttpResponse:
    return HttpResponse()


@csrf_protect  # type: ignore[type-var]  # pyright: ignore[reportArgumentType, reportUntypedFunctionDecorator]
def bad_view(request: int) -> str:
    return ""


@csrf_protect  # type: ignore[type-var]  # pyright: ignore[reportArgumentType, reportUntypedFunctionDecorator]
def bad_view_no_arguments() -> HttpResponse:
    return HttpResponse()
