from collections import OrderedDict
from typing import Any, Iterator, List, Optional, Tuple, Union

from django.core.files.storage import DefaultStorage, FileSystemStorage


def matches_patterns(
    path: str, patterns: Union[OrderedDict, List[str], Tuple[str]] = ...
) -> bool: ...
def get_files(
    storage: Union[DefaultStorage, FileSystemStorage],
    ignore_patterns: List[str] = ...,
    location: str = ...,
) -> Iterator[str]: ...
def check_settings(base_url: Optional[str] = ...) -> None: ...
