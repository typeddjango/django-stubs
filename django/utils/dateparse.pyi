from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import Optional


def parse_date(value: str) -> Optional[date]: ...


def parse_datetime(value: str) -> datetime: ...


def parse_duration(value: str) -> Optional[timedelta]: ...


def parse_time(value: str) -> Optional[time]: ...