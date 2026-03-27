from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpRequest, HttpResponse
from typing_extensions import assert_type

# atomic as context manager
with atomic():
    pass
with atomic(using="mydb"):
    pass
with atomic(using="mydb", savepoint=False):
    pass
with atomic(using="mydb", savepoint=False, durable=True):
    pass


# atomic as bare decorator preserves function type
@atomic
def func(x: int) -> list[object]:
    return []


assert_type(func(1), list[object])


# atomic with args preserves function type
@atomic(using="bla", savepoint=False)
def func2(x: int) -> list[object]:
    return []


assert_type(func2(1), list[object])


# non_atomic_requests bare preserves function type
@non_atomic_requests
def view_func(request: HttpRequest) -> HttpResponse: ...


assert_type(view_func(HttpRequest()), HttpResponse)


# non_atomic_requests with extra args
@non_atomic_requests
def view_func2(request: HttpRequest, arg: str) -> HttpResponse: ...


assert_type(view_func2(HttpRequest(), "test"), HttpResponse)
