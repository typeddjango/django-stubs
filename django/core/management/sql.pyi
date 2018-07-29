from django.core.management.color import Style
from django.db.backends.sqlite3.base import DatabaseWrapper
from typing import List


def emit_post_migrate_signal(verbosity: int, interactive: bool, db: str, **kwargs) -> None: ...


def emit_pre_migrate_signal(verbosity: int, interactive: bool, db: str, **kwargs) -> None: ...


def sql_flush(
    style: Style,
    connection: DatabaseWrapper,
    only_django: bool = ...,
    reset_sequences: bool = ...,
    allow_cascade: bool = ...
) -> List[str]: ...