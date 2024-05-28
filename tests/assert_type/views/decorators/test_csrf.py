from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_protect


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


@csrf_protect  # type: ignore  # pyright: ignore
def bad_view(request: int) -> str:
    return ""


@csrf_protect  # type: ignore  # pyright: ignore
def bad_view_no_arguments() -> HttpResponse:
    return HttpResponse()
