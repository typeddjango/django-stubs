from datetime import (
    date,
    datetime,
)
from typing import (
    Optional,
    Union,
)


def apnumber(value: str) -> str: ...


def intcomma(value: Optional[Union[str, float]], use_l10n: bool = ...) -> str: ...


def intword(value: Optional[str]) -> Optional[str]: ...


def naturalday(value: Optional[date], arg: None = ...) -> Optional[str]: ...


def naturaltime(value: datetime) -> str: ...


def ordinal(value: Optional[str]) -> Optional[str]: ...