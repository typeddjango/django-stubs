from typing import Any, Optional

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    stderr: django.core.management.base.OutputWrapper
    stdout: django.core.management.base.OutputWrapper
    style: django.core.management.color.Style
    help: str = ...
    def handle(self, **options: Any) -> None: ...
