from typing import Any, Iterable, Sequence

from django.core.checks import CheckMessage

def check_database_backends(databases: Iterable[str] | None = ..., **kwargs: Any) -> Sequence[CheckMessage]: ...
