from typing import Any, Optional

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from django.db.models.deletion import Collector

from ...management import get_contenttypes_and_models

class Command(BaseCommand):
    stderr: django.core.management.base.OutputWrapper
    stdout: django.core.management.base.OutputWrapper
    style: django.core.management.color.Style
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, **options: Any) -> None: ...

class NoFastDeleteCollector(Collector):
    data: collections.OrderedDict
    dependencies: Dict[Any, Any]
    fast_deletes: List[Any]
    field_updates: Dict[Any, Any]
    using: str
    def can_fast_delete(self, *args: Any, **kwargs: Any) -> bool: ...
