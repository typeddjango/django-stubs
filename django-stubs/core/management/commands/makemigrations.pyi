from typing import Any

from django.core.management.base import BaseCommand
from django.db.migrations.loader import MigrationLoader

class Command(BaseCommand):
    verbosity: int
    interactive: bool
    dry_run: bool
    merge: bool
    empty: bool
    migration_name: str
    include_header: bool
    def write_migration_files(self, changes: dict[str, Any]) -> None: ...
    def handle_merge(self, loader: MigrationLoader, conflicts: dict[str, Any]) -> None: ...
