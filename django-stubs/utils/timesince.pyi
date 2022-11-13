from datetime import date
from typing import Any

TIME_STRINGS: dict[str, str]
TIMESINCE_CHUNKS: Any

def timesince(
    d: date,
    now: date | None = ...,
    reversed: bool = ...,
    time_strings: dict[str, str] | None = ...,
    depth: int = ...,
) -> str: ...
def timeuntil(d: date, now: date | None = ..., time_strings: dict[str, str] | None = ..., depth: int = ...) -> str: ...
