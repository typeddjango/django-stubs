import enum
import sys
from typing import Any, TypeVar, type_check_only

from typing_extensions import Self, TypeAlias

_Self = TypeVar("_Self")

if sys.version_info >= (3, 11):
    _enum_property = enum.property
    EnumType = enum.EnumType
    IntEnum = enum.IntEnum
    StrEnum = enum.StrEnum
else:
    _enum_property = property
    EnumType = enum.EnumMeta

    class ReprEnum(enum.Enum): ...
    class IntEnum(int, ReprEnum): ...
    class StrEnum(str, ReprEnum): ...

class ChoicesMeta(EnumType):
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

ChoicesType: TypeAlias = ChoicesMeta

class Choices(enum.Enum, metaclass=ChoicesType):
    @property
    def label(self) -> str: ...
    @_enum_property
    def value(self) -> Any: ...
    @property
    def do_not_call_in_templates(self) -> bool: ...

# fake, to keep simulate class properties
@type_check_only
class _IntegerChoicesMeta(ChoicesType):
    @property
    def choices(self) -> list[tuple[int, str]]: ...
    @property
    def values(self) -> list[int]: ...

class IntegerChoices(Choices, IntEnum, metaclass=_IntegerChoicesMeta):
    def __new__(cls, value: int) -> Self: ...
    @_enum_property
    def value(self) -> int: ...

# fake, to keep simulate class properties
@type_check_only
class _TextChoicesMeta(ChoicesType):
    @property
    def choices(self) -> list[tuple[str, str]]: ...
    @property
    def values(self) -> list[str]: ...

class TextChoices(Choices, StrEnum, metaclass=_TextChoicesMeta):
    def __new__(cls, value: str | tuple[str, str]) -> Self: ...
    @_enum_property
    def value(self) -> str: ...
