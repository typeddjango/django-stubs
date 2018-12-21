from typing import Any, Optional

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.base import CommandParser
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    stderr: django.core.management.base.OutputWrapper
    stdout: django.core.management.base.OutputWrapper
    style: django.core.management.color.Style
    help: str = ...
    def add_arguments(self, parser: CommandParser) -> None: ...
    def get_handler(self, *args: Any, **options: Any) -> StaticFilesHandler: ...
