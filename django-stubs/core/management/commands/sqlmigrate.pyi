from django.apps import apps as apps
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections
from django.db.migrations.loader import AmbiguityError as AmbiguityError, MigrationLoader as MigrationLoader
from typing import Any

class Command(BaseCommand):
    output_transaction: bool = ...
    def execute(self, *args: Any, **options: Any): ...
