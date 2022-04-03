from decimal import Decimal
from typing import Iterable, Optional, Union

def format(
    number: Union[Decimal, float, str],
    decimal_sep: str,
    decimal_pos: Optional[int] = ...,
    grouping: Union[int, Iterable[int]] = ...,
    thousand_sep: str = ...,
    force_grouping: bool = ...,
    use_l10n: Optional[bool] = ...,
) -> str: ...
