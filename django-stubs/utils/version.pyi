from typing import (
    Optional,
    Tuple,
)


def get_complete_version(version: Optional[Tuple[int, int, int, str, int]] = ...) -> Tuple[int, int, int, str, int]: ...


def get_docs_version(version: None = ...) -> str: ...


def get_git_changeset() -> str: ...


def get_main_version(version: Tuple[int, int, int, str, int] = ...) -> str: ...


def get_version(version: Optional[Tuple[int, int, int, str, int]] = ...) -> str: ...