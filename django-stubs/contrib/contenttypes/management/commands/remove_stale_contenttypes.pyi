from _typeshed import Unused
from typing import Literal

from django.db.models.deletion import Collector

from django.core.management import BaseCommand


class Command(BaseCommand): ...

class NoFastDeleteCollector(Collector):
    def can_fast_delete(self, *args: Unused, **kwargs: Unused) -> Literal[False]: ...
