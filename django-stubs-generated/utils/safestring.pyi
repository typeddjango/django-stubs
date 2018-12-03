from typing import Any, Callable, Optional, Union

from django.forms.boundfield import BoundField

class SafeData:
    def __html__(self) -> SafeText: ...

class SafeBytes(bytes, SafeData):
    def __add__(self, rhs: Any): ...

class SafeText(str, SafeData):
    def __add__(self, rhs: str) -> str: ...

SafeString = SafeText

def mark_safe(s: Union[Callable, BoundField, str]) -> Union[Callable, BoundField, str]: ...
