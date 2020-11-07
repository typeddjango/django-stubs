from django.conf import settings as settings
from django.core.cache import caches as caches
from django.core.cache.backends.db import BaseDatabaseCache as BaseDatabaseCache
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, DatabaseError as DatabaseError, connections as connections, models as models, router as router, transaction as transaction
from typing import Any

class Command(BaseCommand):
    verbosity: int = ...
    def handle(self, *tablenames: Any, **options: Any) -> None: ...
    def create_table(self, database: Any, tablename: Any, dry_run: Any) -> None: ...
