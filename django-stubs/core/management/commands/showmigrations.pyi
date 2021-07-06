from typing import Any, List, Optional

from django.apps import apps as apps
from django.core.management.base import BaseCommand as BaseCommand
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS
from django.db import connections as connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.loader import MigrationLoader as MigrationLoader

class Command(BaseCommand):
    verbosity: int = ...
    def show_list(self, connection: BaseDatabaseWrapper, app_names: Optional[List[str]] = ...) -> None: ...
    def show_plan(self, connection: BaseDatabaseWrapper, app_names: Optional[List[str]] = ...) -> None: ...
