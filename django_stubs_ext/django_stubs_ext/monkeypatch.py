from typing import Generic, List, Optional, Type, TypeVar

import django
from django.contrib.admin import ModelAdmin

_T = TypeVar("_T")


class MPGeneric(Generic[_T]):
    """Create a data class to hold metadata about the gneric classes needing monkeypatching.

    The `version` param is optional, and a value of `None` means that the monkeypatch is
    version-independent.

    This is slightly overkill for our purposes, but useful for future-proofing against any
    possible issues we may run into with this method.
    """

    version: Optional[int]
    cls: Type[_T]

    def __init__(self, cls: Type[_T], version: Optional[int] = None) -> None:
        """Set the data fields, basic constructor."""
        self.version = version
        self.cls = cls


# certain django classes need to be generic, but lack the __class_getitem__ dunder needed to
# annotate them: https://github.com/typeddjango/django-stubs/issues/507
# this list stores them so `monkeypatch` can fix them when called
__need_generic: List[MPGeneric] = [
    MPGeneric(ModelAdmin),
]


# currently just adds the __class_getitem__ dunder. if more monkeypatching is needed, add it here
def monkeypatch() -> None:
    """Monkey patch django as necessary to work properly with mypy."""
    for el in filter(lambda x: django.VERSION[0] == x.version or x.version is None, __need_generic):
        el.cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)


__all__ = ["monkeypatch"]
