from collections.abc import Callable
from typing import List

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpRequest, HttpResponse


@atomic
def func1(x: int) -> List[int]: ...


x1: Callable[[int], List[int]] = func1
func1("str")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


@atomic(using="bla", savepoint=False)
def func2(x: int) -> List[int]: ...


x1 = func2
func2("str")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


@atomic()
def func3(param1: str, param2: int) -> bool: ...


x2: Callable[[str, int], bool] = func3
func3(1.0, 2.0)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


class ClassWithAtomicMethod:
    @atomic
    def method1(self, abc: int) -> str: ...
    @atomic(savepoint=True)
    def method2(self) -> None: ...
    @atomic(using="db", savepoint=True)
    def method3(self, myparam: str) -> int: ...


# E: Argument 1 to "atomic_method1" of "ClassWithAtomicMethod" has incompatible type "str"; expected "int"
ClassWithAtomicMethod().method1("abc")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

x3: Callable[[int], str] = ClassWithAtomicMethod().method1
ClassWithAtomicMethod().method1(1.0)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

x4: Callable[[], None] = ClassWithAtomicMethod().method2
ClassWithAtomicMethod().method2(1.0)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

x5: Callable[[str], int] = ClassWithAtomicMethod().method3
ClassWithAtomicMethod().method3(1.0)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


with atomic():
    ...
with atomic(using="mydb", savepoint=False, durable=True):
    ...


@non_atomic_requests
def view_func1(request: HttpRequest) -> HttpResponse: ...


x6: Callable[[HttpRequest], HttpResponse] = view_func1
view_func1(1)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


@non_atomic_requests
def view_func2(request: HttpRequest, arg: str) -> HttpResponse: ...


x7: Callable[[HttpRequest, str], HttpResponse] = view_func2
view_func2(1, 1.0)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
