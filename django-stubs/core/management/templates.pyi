from django.core.management.base import CommandParser


class TemplateCommand:
    def add_arguments(self, parser: CommandParser) -> None: ...