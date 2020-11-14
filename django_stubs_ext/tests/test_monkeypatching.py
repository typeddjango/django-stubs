import pytest

import django_stubs_ext
from django_stubs_ext.monkeypatch import _need_generic, _VersionSpec, django


@pytest.fixture(scope="function")
def make_generic_classes(request, monkeypatch):
    def fin():
        for el in _need_generic:
            delattr(el.cls, "__class_getitem__")

    def factory(django_version=None):
        if django_version is not None:
            monkeypatch.setattr(django, "VERSION", django_version)
        django_stubs_ext.monkeypatch()

    request.addfinalizer(fin)
    return factory


def test_patched_generics(make_generic_classes) -> None:
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
    make_generic_classes,
) -> None:
    """Test version speicific types."""
    make_generic_classes(django_version)

    for el in _need_generic:
        if el.version is not None and el.version[:2] <= django_version:
            assert el.cls[int] is el.cls
