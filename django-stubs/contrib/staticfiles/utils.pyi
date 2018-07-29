from collections import OrderedDict
from django.core.files.storage import (
    DefaultStorage,
    FileSystemStorage,
)
from typing import (
    Iterator,
    List,
    Tuple,
    Union,
)


def check_settings(base_url: str = ...) -> None: ...


def get_files(
    storage: Union[FileSystemStorage, DefaultStorage],
    ignore_patterns: List[str] = ...,
    location: str = ...
) -> Iterator[str]: ...


def matches_patterns(path: str, patterns: Union[OrderedDict, List[str], Tuple[str]] = ...) -> bool: ...