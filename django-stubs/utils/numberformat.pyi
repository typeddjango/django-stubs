from decimal import Decimal
from typing import Any, Optional, Tuple, Union


def format(
    number: Union[Decimal, float, int, str],
    decimal_sep: str,
    decimal_pos: Optional[int] = ...,
    grouping: Union[Tuple[int, int, int], int] = ...,
    thousand_sep: str = ...,
    force_grouping: bool = ...,
    use_l10n: Optional[bool] = ...,
) -> str: ...
