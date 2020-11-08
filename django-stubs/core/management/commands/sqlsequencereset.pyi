from django.core.management.base import AppCommand as AppCommand
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections

class Command(AppCommand): ...
