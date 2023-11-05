import enum
import sys
from typing import Any, TypeVar

from typing_extensions import Self

_Self = TypeVar("_Self")

if sys.version_info >= (3, 11):
    _enum_property = enum.property
else:
    _enum_property = property

class ChoicesMeta(enum.EnumMeta):
    # There's a contradiction between mypy and PYI019 regarding metaclasses. Where mypy
    # disallows 'typing_extensions.Self' on metaclasses, while PYI019 try to enforce
    # 'typing_extensions.Self' for '__new__' methods.. We've chosen to ignore the
    # linter and trust mypy.
    def __new__(
        metacls: type[_Self], classname: str, bases: tuple[type, ...], classdict: enum._EnumDict, **kwds: Any
    ) -> _Self: ...  # noqa: PYI019
    def __contains__(self, member: Any) -> bool: ...
    @property
    def names(self) -> list[str]: ...
    @property
    def choices(self) -> list[tuple[Any, str]]: ...
    @property
    def labels(self) -> list[str]: ...
    @property
    def values(self) -> list[Any]: ...

class Choices(enum.Enum, metaclass=ChoicesMeta):
    @property
    def label(self) -> str: ...
    @_enum_property
    def value(self) -> Any: ...
    @property
    def do_not_call_in_templates(self) -> bool: ...

# fake, to keep simulate class properties
class _IntegerChoicesMeta(ChoicesMeta):
    @property
    def choices(self) -> list[tuple[int, str]]: ...
    @property
    def values(self) -> list[int]: ...

class IntegerChoices(int, Choices, metaclass=_IntegerChoicesMeta):
    def __new__(cls, value: int) -> Self: ...
    @_enum_property
    def value(self) -> int: ...

# fake, to keep simulate class properties
class _TextChoicesMeta(ChoicesMeta):
    @property
    def choices(self) -> list[tuple[str, str]]: ...
    @property
    def values(self) -> list[str]: ...

class TextChoices(str, Choices, metaclass=_TextChoicesMeta):
    def __new__(cls, value: str) -> Self: ...
    @_enum_property
    def value(self) -> str: ...
