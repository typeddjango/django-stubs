from datetime import date
from datetime import datetime as datetime
from typing import Any, Callable, Dict, SupportsInt, Tuple, Type

from django import template

register: template.Library

def ordinal(value: str | SupportsInt | None) -> str | None: ...
def intcomma(value: str | SupportsInt | None, use_l10n: bool = ...) -> str: ...

intword_converters: Tuple[Tuple[int, Callable]]

def intword(value: str | SupportsInt | None) -> int | str | None: ...
def apnumber(value: str | SupportsInt | None) -> int | str | None: ...
def naturalday(value: date | str | None, arg: str | None = ...) -> str | None: ...
def naturaltime(value: datetime) -> str: ...

class NaturalTimeFormatter:
    time_strings: Dict[str, str]
    past_substrings: Dict[str, str]
    future_substrings: Dict[str, str]
    @classmethod
    def string_for(cls: Type[NaturalTimeFormatter], value: Any) -> Any: ...
