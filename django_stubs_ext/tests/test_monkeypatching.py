from contextlib import suppress
from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch
from typing_extensions import Protocol

import django_stubs_ext
from django_stubs_ext import patch
from django_stubs_ext.patch import _need_generic, _VersionSpec


class _MakeGenericClasses(Protocol):
    """Used to represent a type of ``make_generic_classes`` fixture."""

    def __call__(self, django_version: Optional[_VersionSpec] = None) -> None:
        ...


@pytest.fixture(scope="function")
def make_generic_classes(
    request: FixtureRequest,
    monkeypatch: MonkeyPatch,
) -> _MakeGenericClasses:
    def fin() -> None:
        for el in _need_generic:
            with suppress(AttributeError):
                delattr(el.cls, "__class_getitem__")

    def factory(django_version: Optional[_VersionSpec] = None) -> None:
        if django_version is not None:
            monkeypatch.setattr(patch, "VERSION", django_version)
        django_stubs_ext.monkeypatch()

    request.addfinalizer(fin)
    return factory


def test_patched_generics(make_generic_classes: _MakeGenericClasses) -> None:
    """Test that the generics actually get patched."""
    make_generic_classes()

    for el in _need_generic:
        if el.version is None:
            assert el.cls[type] is el.cls  # `type` is arbitrary


@pytest.mark.parametrize(
    "django_version",
    [
        (2, 2),
        (3, 0),
        (3, 1),
        (3, 2),
    ],
)
def test_patched_version_specific(
    django_version: _VersionSpec,
    make_generic_classes: _MakeGenericClasses,
) -> None:
    """Test version speicific types."""
    make_generic_classes(django_version)

    for el in _need_generic:
        if el.version is not None and django_version <= el.version:
            assert el.cls[int] is el.cls
