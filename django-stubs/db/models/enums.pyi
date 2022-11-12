import enum
import sys
from typing import Any, List, Tuple

if sys.version_info >= (3, 11):
    enum_property = enum.property
else:
    enum_property = property

class ChoicesMeta(enum.EnumMeta):
    names: List[str]
    choices: List[Tuple[Any, str]]
    labels: List[str]
    values: List[Any]
    def __contains__(self, member: Any) -> bool: ...

class Choices(enum.Enum, metaclass=ChoicesMeta):
    def __str__(self) -> str: ...
    @property
    def label(self) -> str: ...
    @enum_property
    def value(self) -> Any: ...

# fake
class _IntegerChoicesMeta(ChoicesMeta):
    names: List[str]
    choices: List[Tuple[int, str]]
    labels: List[str]
    values: List[int]

class IntegerChoices(int, Choices, metaclass=_IntegerChoicesMeta):
    @enum_property
    def value(self) -> int: ...

# fake
class _TextChoicesMeta(ChoicesMeta):
    names: List[str]
    choices: List[Tuple[str, str]]
    labels: List[str]
    values: List[str]

class TextChoices(str, Choices, metaclass=_TextChoicesMeta):
    @enum_property
    def value(self) -> str: ...
