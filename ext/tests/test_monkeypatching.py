from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Generic, Protocol, get_args, get_origin

import pytest
from django.db.models import Model
from django.forms.models import ModelForm
from django.views import View
from typing_extensions import TypeVar

import django_stubs_ext
from django_stubs_ext import patch
from django_stubs_ext.patch import _need_generic, _VersionSpec

if TYPE_CHECKING:
    from collections.abc import Iterable


class _MakeGenericClasses(Protocol):
    """Used to represent a type of ``make_generic_classes`` fixture."""

    def __call__(
        self,
        django_version: _VersionSpec | None = None,
        extra_classes: Iterable[type] | None = None,
    ) -> None: ...


@pytest.fixture(scope="function")
def make_generic_classes(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> _MakeGenericClasses:
    _extra_classes: list[type] = []

    def fin() -> None:
        for el in _need_generic:
            with suppress(AttributeError):
                delattr(el.cls, "__class_getitem__")
        for cls in _extra_classes:
            with suppress(AttributeError):
                delattr(cls, "__class_getitem__")
        _extra_classes.clear()

    def factory(
        django_version: _VersionSpec | None = None,
        extra_classes: Iterable[type] | None = None,
    ) -> None:
        if extra_classes:
            _extra_classes.extend(extra_classes)
        if django_version is not None:
            monkeypatch.setattr(patch, "VERSION", django_version)
        django_stubs_ext.monkeypatch(extra_classes=extra_classes)

    request.addfinalizer(fin)
    return factory


def test_patched_generics(make_generic_classes: _MakeGenericClasses) -> None:
    """Test that the generics actually get patched."""
    make_generic_classes()

    for el in _need_generic:
        if el.version is None:
            assert el.cls[type] is el.cls  # `type` is arbitrary

    class TestForm(ModelForm[Model]):
        pass


def test_patched_extra_classes_generics(make_generic_classes: _MakeGenericClasses) -> None:
    """Test that the generics actually get patched for extra classes."""

    class _NotGeneric:
        pass

    extra_classes = [_NotGeneric]
    make_generic_classes(django_version=None, extra_classes=extra_classes)

    for cls in extra_classes:
        assert cls[type] is cls  # type: ignore[misc]

    class _TestGeneric(_NotGeneric[Model]):  # type: ignore[type-arg]
        pass


def test_patched_class_real_generic_subclass(make_generic_classes: _MakeGenericClasses) -> None:
    """Test that real `Generic` subclasses of patched classes keep runtime parametrization.    """
    make_generic_classes()

    assert View[int] is View

    _T = TypeVar("_T")

    class _Controller(View, Generic[_T]):
        pass

    alias = _Controller[int]
    assert get_origin(alias) is _Controller
    assert get_args(alias) == (int,)

    class _Concrete(_Controller[int]):
        pass

    assert _Concrete.__orig_bases__ == (_Controller[int],)  # type: ignore[attr-defined]

    class _PlainView(View):
        pass

    assert _PlainView[int] is _PlainView  # type: ignore[misc]

    class _CustomGetitem:
        def __class_getitem__(cls, item: object) -> object:
            return ("custom", cls, item)

    class _WithCustom(View, _CustomGetitem):
        pass

    assert _WithCustom[int] == ("custom", _WithCustom, int)  # type: ignore[misc]


@pytest.mark.parametrize(
    "django_version",
    [
        (2, 2),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
    ],
)
def test_patched_version_specific(
    django_version: _VersionSpec,
    make_generic_classes: _MakeGenericClasses,
) -> None:
    """Test version specific types."""
    make_generic_classes(django_version)

    for el in _need_generic:
        if el.version is not None and django_version <= el.version:
            assert el.cls[int] is el.cls
