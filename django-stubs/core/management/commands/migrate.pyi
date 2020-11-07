from django.apps import apps as apps
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError, no_translations as no_translations
from django.core.management.sql import emit_post_migrate_signal as emit_post_migrate_signal, emit_pre_migrate_signal as emit_pre_migrate_signal
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections, router as router
from django.db.migrations.autodetector import MigrationAutodetector as MigrationAutodetector
from django.db.migrations.executor import MigrationExecutor as MigrationExecutor
from django.db.migrations.loader import AmbiguityError as AmbiguityError
from django.db.migrations.state import ModelState as ModelState, ProjectState as ProjectState
from django.utils.module_loading import module_has_submodule as module_has_submodule
from django.utils.text import Truncator as Truncator
from typing import Any, Optional

class Command(BaseCommand):
    verbosity: int = ...
    interactive: Any = ...
    start: Any = ...
    def migration_progress_callback(self, action: Any, migration: Optional[Any] = ..., fake: bool = ...) -> None: ...
    def sync_apps(self, connection: Any, app_labels: Any): ...
    @staticmethod
    def describe_operation(operation: Any, backwards: Any): ...
