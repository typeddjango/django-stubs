from django.core.management.base import CommandParser
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.migration import Migration
from typing import (
    Dict,
    List,
    Set,
)


class Command:
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle_merge(self, loader: MigrationLoader, conflicts: Dict[str, Set[str]]) -> None: ...
    def write_migration_files(self, changes: Dict[str, List[Migration]]) -> None: ...