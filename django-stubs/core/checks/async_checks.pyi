from typing import Any, List, Optional, Sequence

from django.core.checks.messages import CheckMessage

from django.apps.config import AppConfig

E001: Any

def check_async_unsafe(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[CheckMessage]: ...
