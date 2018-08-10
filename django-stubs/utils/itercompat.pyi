from tempfile import _TemporaryFileWrapper
from typing import Any, List, Optional, Tuple, Union

from django.core.checks.messages import CheckMessage


def is_iterable(
    x: Optional[
        Union[
            List[List[Union[List[List[Union[List[List[str]], str]]], str]]],
            List[
                Tuple[
                    Union[Tuple[Tuple[int, str], Tuple[int, str]], str],
                    Union[Tuple[Tuple[int, str], Tuple[int, str]], str],
                ]
            ],
            List[Tuple[int, int, int]],
            List[CheckMessage],
            List[int],
            List[str],
            Tuple[
                Tuple[
                    Union[Tuple[Tuple[int, str], Tuple[int, str]], str],
                    Union[
                        Tuple[Tuple[int, str], Tuple[int, str]],
                        Tuple[Tuple[str, str], Tuple[str, str]],
                        str,
                    ],
                ]
            ],
            Tuple[str, str, str],
            Tuple[_TemporaryFileWrapper, _TemporaryFileWrapper],
            int,
        ]
    ]
) -> bool: ...
