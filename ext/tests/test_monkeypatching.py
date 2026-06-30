from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Protocol

import pytest
from django.db.models import Model
from django.forms.models import ModelForm

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
