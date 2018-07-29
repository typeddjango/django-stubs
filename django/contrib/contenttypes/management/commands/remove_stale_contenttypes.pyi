from django.core.management.base import CommandParser


class Command:
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, **options) -> None: ...


class NoFastDeleteCollector:
    def can_fast_delete(self, *args, **kwargs) -> bool: ...