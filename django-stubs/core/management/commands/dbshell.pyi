from django.core.management.base import (
    BaseCommand as BaseCommand,
    CommandError as CommandError,
    CommandParser as CommandParser,
)
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections

class Command(BaseCommand): ...
