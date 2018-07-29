from datetime import date
from typing import Optional


def timesince(
    d: date,
    now: Optional[date] = ...,
    reversed: bool = ...,
    time_strings: None = ...
) -> str: ...


def timeuntil(d: date, now: Optional[date] = ..., time_strings: None = ...) -> str: ...