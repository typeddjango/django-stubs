from django.forms.boundfield import BoundField
from typing import (
    Callable,
    Union,
)


def _safety_decorator(safety_marker: Callable, func: Callable) -> Callable: ...


def mark_safe(
    s: Union[str, BoundField, Callable]
) -> Union[SafeText, BoundField, Callable]: ...


class SafeData:
    def __html__(self) -> SafeText: ...


class SafeText:
    def __add__(self, rhs: str) -> str: ...
    def __str__(self) -> SafeText: ...