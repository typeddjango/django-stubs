from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, ClassVar

from django.contrib.auth.models import User
from django.utils.functional import Promise, SimpleLazyObject, cached_property, classproperty, lazystr
from typing_extensions import assert_type, override

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise


# cached_property: class vs instance attributes
class Foo:
    @cached_property
    def attr(self) -> list[str]: ...

    @cached_property  # type: ignore[misc]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    def attr2(self, arg2: str) -> list[str]: ...


f = Foo()
assert_type(f.attr, list[str])
f.attr.func  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue,reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


# May be overridden by @property
class Bar(Foo):
    @property
    @override
    def attr(self) -> list[str]: ...  # pyright: ignore[reportIncompatibleVariableOverride]


# May be overridden by ClassVar
class Quux(Foo):
    attr: ClassVar[list[str]] = []  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]


# ClassVar may not be overridden by cached_property
class Baz(Quux):
    @cached_property
    @override
    def attr(self) -> list[str]: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-attribute-override]


# str promise proxy

s = lazystr("asd")

assert_type(s.format("asd"), str)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
assert_type(s.capitalize(), str)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
assert_type(s + "bar", str)
assert_type("foo" + s, str)
assert_type(s % "asd", str)

s.nonsense  # type: ignore[attr-defined]  # pyrefly: ignore[no-attribute]


def test_str_or_promise(f2: StrOrPromise) -> None:
    assert_type(f2.format("asd"), str)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(f2 + "asd", str)
    assert_type("asd" + f2, str)


def foo(content: str) -> None: ...


def bar(content: Promise) -> None: ...


foo(s)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
bar(s)


lazy_user: SimpleLazyObject[User] = SimpleLazyObject(User)
assert_type(lazy_user, SimpleLazyObject[User])

assert_type(copy.copy(lazy_user), SimpleLazyObject[User])
assert_type(copy.deepcopy(lazy_user), SimpleLazyObject[User])


class Bam:
    @classproperty
    def attr(cls: Any) -> str: ...


assert_type(Bam.attr, str)


class Sub(Bam):
    def method(self) -> None:
        assert_type(self.attr, str)
