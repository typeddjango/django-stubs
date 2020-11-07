from django.apps import apps as apps
from django.core import checks as checks
from django.core.checks.registry import registry as registry
from django.core.management.base import BaseCommand as BaseCommand, CommandError as CommandError
from typing import Any

class Command(BaseCommand):
    def handle(self, *app_labels: Any, **options: Any) -> None: ...
