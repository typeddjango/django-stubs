from django.apps import apps as apps
from django.core.management.base import (
    BaseCommand as BaseCommand,
    CommandError as CommandError,
    no_translations as no_translations,
)
from django.core.management.sql import (
    emit_post_migrate_signal as emit_post_migrate_signal,
    emit_pre_migrate_signal as emit_pre_migrate_signal,
)
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections, router as router
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.autodetector import MigrationAutodetector as MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor as MigrationExecutor
from django.db.migrations.loader import AmbiguityError as AmbiguityError
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ModelState as ModelState, ProjectState as ProjectState
from django.utils.module_loading import module_has_submodule as module_has_submodule
from django.utils.text import Truncator as Truncator
from typing import Any, List, Optional

class Command(BaseCommand):
    verbosity: int = ...
    interactive: bool = ...
    start: float = ...
    def migration_progress_callback(self, action: str, migration: Optional[Any] = ..., fake: bool = ...) -> None: ...
    def sync_apps(self, connection: BaseDatabaseWrapper, app_labels: List[str]) -> None: ...
    @staticmethod
    def describe_operation(operation: Operation, backwards: bool) -> str: ...
