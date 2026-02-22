from argparse import Action, ArgumentParser, Namespace
from collections.abc import Sequence
from typing import Any

from django.core.management.base import BaseCommand

class LayerOptionAction(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None: ...

class ListOptionAction(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None: ...

class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None: ...
    def handle(self, *args: Any, **options: Any) -> str: ...
