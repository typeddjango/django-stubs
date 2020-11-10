import django_stubs_ext
from django_stubs_ext.monkeypatch import _need_generic

django_stubs_ext.monkeypatch()


def test_patched_generics():
    """Test that the generics actually get patched."""
    for el in _need_generic:
        # This only throws an exception if the monkeypatch failed
        el.cls[int]  # doesn't need to be int, can be any class
