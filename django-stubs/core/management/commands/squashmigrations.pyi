from django.apps import apps as apps
from django.conf import settings as settings
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections, migrations as migrations
from django.db.migrations.migration import Migration
from django.db.migrations.loader import AmbiguityError as AmbiguityError, MigrationLoader as MigrationLoader
from django.db.migrations.migration import SwappableTuple as SwappableTuple
from django.db.migrations.optimizer import MigrationOptimizer as MigrationOptimizer
from django.db.migrations.writer import MigrationWriter as MigrationWriter
from django.utils.version import get_docs_version as get_docs_version

class Command(BaseCommand):
    verbosity: int = ...
    interactive: bool = ...
    def find_migration(self, loader: MigrationLoader, app_label: str, name: str) -> Migration: ...
