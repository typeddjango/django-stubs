import builtins
from contextlib import suppress
from typing import Iterable, Optional

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch
from django.db.models import Model
from django.forms.models import ModelForm
from django.views import View
from typing_extensions import Protocol

import django_stubs_ext
from django_stubs_ext import patch
from django_stubs_ext.patch import _need_generic, _VersionSpec


class _MakeGenericClasses(Protocol):
    """Used to represent a type of ``make_generic_classes`` fixture."""

    def __call__(
        self,
        django_version: Optional[_VersionSpec] = None,
        extra_classes: Optional[Iterable[type]] = None,
    ) -> None:
        ...


@pytest.fixture(scope="function")
def make_generic_classes(
    request: FixtureRequest,
    monkeypatch: MonkeyPatch,
) -> _MakeGenericClasses:
    _extra_classes: list[type] = []

    def fin() -> None:
        for el in _need_generic:
            with suppress(AttributeError):
                delattr(el.cls, "__class_getitem__")
        for cls in _extra_classes:
            with suppress(AttributeError):
                delattr(cls, "__class_getitem__")

    def factory(
        django_version: Optional[_VersionSpec] = None,
        extra_classes: Optional[Iterable[type]] = None,
    ) -> None:
        if extra_classes:
            _extra_classes.extend(extra_classes)
        if django_version is not None:
            monkeypatch.setattr(patch, "VERSION", django_version)
        django_stubs_ext.monkeypatch(extra_classes)

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


def test_patched_extra_classes_generics(
    make_generic_classes: _MakeGenericClasses,
) -> None:
    """Test that the generics actually get patched for extra classes."""
    extra_classes = [View]

    make_generic_classes(django_version=None, extra_classes=extra_classes)

    for cls in extra_classes:
        assert cls[type] is cls  # type: ignore[misc]

    class TestView(View[Model]):  # type: ignore[type-arg]
        pass


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


def test_mypy_builtins_not_patched_globally(
    make_generic_classes: _MakeGenericClasses,
) -> None:
    """Ensures that builtins are not patched with `mypy` specific helpers.

    This should only happend during `django.setup()`
    (https://github.com/typeddjango/django-stubs/issues/609).
    """
    make_generic_classes()

    assert not hasattr(builtins, "reveal_type")
    assert not hasattr(builtins, "reveal_locals")
