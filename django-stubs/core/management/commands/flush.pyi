from django.apps import apps as apps
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError
from django.core.management.color import Style, no_style as no_style
from django.core.management.sql import emit_post_migrate_signal as emit_post_migrate_signal, sql_flush as sql_flush
from django.db import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, connections as connections
from typing import Tuple

class Command(BaseCommand):
    stealth_options: Tuple[str] = ...
    style: Style = ...
