from datetime import (
    date,
    time,
)
from decimal import Decimal
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Union,
)


def date_format(
    value: Union[time, date, str],
    format: Optional[str] = ...,
    use_l10n: Optional[bool] = ...
) -> str: ...


def get_format(
    format_type: str,
    lang: Optional[str] = ...,
    use_l10n: Optional[bool] = ...
) -> Union[str, List[str], int]: ...


def get_format_modules(lang: str = ..., reverse: bool = ...) -> List[Any]: ...


def iter_format_modules(lang: str, format_module_path: Optional[str] = ...) -> Iterator[Any]: ...


def localize(value: Any, use_l10n: Optional[bool] = ...) -> Any: ...


def localize_input(value: Any, default: Optional[str] = ...) -> Optional[str]: ...


def number_format(
    value: Union[Decimal, float, str, int],
    decimal_pos: Optional[int] = ...,
    use_l10n: Optional[bool] = ...,
    force_grouping: bool = ...
) -> str: ...


def reset_format_cache() -> None: ...


def sanitize_separators(value: Union[str, int]) -> Union[str, int]: ...


def time_format(
    value: Union[date, time, str],
    format: Optional[str] = ...,
    use_l10n: None = ...
) -> str: ...