from typing import Any, List, Type

from django.contrib.admin import ModelAdmin

# certain django classes need to be generic, but lack the __class_getitem__ dunder needed to
# annotate them: https://github.com/typeddjango/django-stubs/issues/507
# this list stores them so `monkeypatch` can fix them when called
__need_generic: List[Type[Any]] = [
    ModelAdmin,
]


# currently just adds the __class_getitem__ dunder. if more monkeypatching is needed, add it here
def monkeypatch() -> None:
    """Monkey patch django as necessary to work properly with mypy."""
    for cls in __need_generic:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
