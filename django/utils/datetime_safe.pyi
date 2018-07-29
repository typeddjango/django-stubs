from datetime import (
    date,
    datetime,
)
from typing import (
    List,
    Union,
)


def _findall(text: str, substr: str) -> List[int]: ...


def new_date(d: date) -> date: ...


def new_datetime(d: datetime) -> datetime: ...


def strftime(dt: Union[date, datetime], fmt: str) -> str: ...


class date:
    def strftime(self, fmt: str) -> str: ...


class datetime:
    def strftime(self, fmt: str) -> str: ...