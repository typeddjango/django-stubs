from datetime import date
from typing import Any, Dict

TIME_STRINGS: Dict[str, str]
TIMESINCE_CHUNKS: Any

def timesince(
    d: date,
    now: date | None = ...,
    reversed: bool = ...,
    time_strings: Dict[str, str] | None = ...,
    depth: int = ...,
) -> str: ...
def timeuntil(d: date, now: date | None = ..., time_strings: Dict[str, str] | None = ..., depth: int = ...) -> str: ...
