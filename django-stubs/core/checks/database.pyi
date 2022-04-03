from typing import Any, Iterable, Optional, Sequence

from django.core.checks import CheckMessage

def check_database_backends(databases: Optional[Iterable[str]] = ..., **kwargs: Any) -> Sequence[CheckMessage]: ...
