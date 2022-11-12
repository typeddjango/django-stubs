from typing import Any, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import Error

E001: Error

def check_async_unsafe(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> Sequence[Error]: ...
