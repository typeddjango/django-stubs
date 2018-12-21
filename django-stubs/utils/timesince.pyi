from datetime import date
from typing import Any, Optional

TIME_STRINGS: Any
TIMESINCE_CHUNKS: Any

def timesince(d: date, now: Optional[date] = ..., reversed: bool = ..., time_strings: None = ...) -> str: ...
def timeuntil(d: date, now: Optional[date] = ..., time_strings: None = ...) -> str: ...
