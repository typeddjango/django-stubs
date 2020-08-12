from typing import Any, Callable, Dict, TypeVar

from . import Field

_ErrorMessagesToOverride = Dict[str, Any]

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class JSONField(Field[_ST, _GT]):
    empty_strings_allowed: str
    error_messages: _ErrorMessagesToOverride
    def __init__(
        self,
        verbose_name: str = ...,
        name: str = ...,
        encoder: Callable = ...,
        decoder: Callable = ...,
    ): ...
