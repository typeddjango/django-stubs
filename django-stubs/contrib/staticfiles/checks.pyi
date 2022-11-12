from typing import Any, List, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage

def check_finders(app_configs: Sequence[AppConfig] | None = ..., **kwargs: Any) -> List[CheckMessage]: ...
