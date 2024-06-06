from collections.abc import Callable
from typing import List

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpRequest, HttpResponse


@atomic
def func1(x: int) -> List[int]: ...


x1: Callable[[int], List[int]] = func1


@atomic(using="bla", savepoint=False)
def func2(x: int) -> List[int]: ...


x1 = func2


@non_atomic_requests
def view_func1(request: HttpRequest) -> HttpResponse: ...


x2: Callable[[HttpRequest], HttpResponse] = view_func1


@non_atomic_requests
def view_func2(request: HttpRequest, arg: str) -> HttpResponse: ...


x3: Callable[[HttpRequest, str], HttpResponse] = view_func2
