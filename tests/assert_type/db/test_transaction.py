from __future__ import annotations

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
def view_func(request: HttpRequest) -> HttpResponse:
    raise NotImplementedError


assert_type(view_func(HttpRequest()), HttpResponse)


# non_atomic_requests with extra args
@non_atomic_requests
def view_func2(request: HttpRequest, arg: str) -> HttpResponse:
    raise NotImplementedError


assert_type(view_func2(HttpRequest(), "test"), HttpResponse)


# atomic as decorator on class methods
class ClassWithAtomicMethod:
    @atomic
    def atomic_method1(self, abc: int) -> str:
        return ""

    @atomic(savepoint=True)
    def atomic_method2(self) -> None:
        pass

    @atomic(using="db", savepoint=True)
    def atomic_method3(self, myparam: str) -> int:
        return 0


assert_type(ClassWithAtomicMethod().atomic_method1(1), str)
assert_type(ClassWithAtomicMethod().atomic_method3("x"), int)
ClassWithAtomicMethod().atomic_method1("abc")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
