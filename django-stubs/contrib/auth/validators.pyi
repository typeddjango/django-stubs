from collections.abc import Sequence
from typing import Any

from django.core.validators import RegexValidator

class ASCIIUsernameValidator(RegexValidator):
    def deconstruct(obj) -> tuple[str, Sequence[Any], dict[str, Any]]: ...

class UnicodeUsernameValidator(RegexValidator):
    def deconstruct(obj) -> tuple[str, Sequence[Any], dict[str, Any]]: ...
