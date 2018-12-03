from tempfile import _TemporaryFileWrapper
from typing import Any, List, Optional, Tuple, Union

from django.core.checks.messages import CheckMessage

def is_iterable(
    x: Optional[
        Union[
            List[List[Union[List[List[Union[List[List[str]], str]]], str]]],
            List[Tuple[Optional[Union[int, str]], Union[int, str]]],
            List[CheckMessage],
            List[int],
            List[str],
            Tuple[Union[Tuple[str, str], _TemporaryFileWrapper]],
            int,
        ]
    ]
) -> bool: ...
