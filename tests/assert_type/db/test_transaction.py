from collections.abc import Callable

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpRequest, HttpResponse
from typing_extensions import assert_type


@atomic
def func1(x: int, /) -> list[int]: ...


assert_type(func1, Callable[[int], list[int]])


@atomic(using="bla", savepoint=False)
def func2(x: int, /) -> list[int]: ...


assert_type(func2, Callable[[int], list[int]])


@non_atomic_requests
def view_func1(request: HttpRequest, /) -> HttpResponse: ...


assert_type(view_func1, Callable[[HttpRequest], HttpResponse])


@non_atomic_requests
def view_func2(request: HttpRequest, arg: str, /) -> HttpResponse: ...


assert_type(view_func2, Callable[[HttpRequest, str], HttpResponse])
