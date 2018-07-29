from django.core.management.base import CommandParser
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.migrations.migration import Migration
from typing import (
    Any,
    List,
    Optional,
    Set,
)


class Command:
    def _run_checks(self, **kwargs) -> List[Any]: ...
    def add_arguments(self, parser: CommandParser) -> None: ...
    def migration_progress_callback(
        self,
        action: str,
        migration: Optional[Migration] = ...,
        fake: bool = ...
    ) -> None: ...
    def sync_apps(self, connection: DatabaseWrapper, app_labels: Set[str]) -> None: ...