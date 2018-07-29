from decimal import Decimal
from typing import (
    Optional,
    Tuple,
    Union,
)


def format(
    number: Union[float, Decimal, str],
    decimal_sep: str,
    decimal_pos: Optional[int] = ...,
    grouping: Union[Tuple[int, int, int, int, int], Tuple[int, int, int], int] = ...,
    thousand_sep: str = ...,
    force_grouping: bool = ...,
    use_l10n: Optional[bool] = ...
) -> str: ...