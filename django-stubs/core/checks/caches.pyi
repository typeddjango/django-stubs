from typing import Any, List, Optional, Sequence

from django.core.checks.messages import Error

from django.apps.config import AppConfig

E001: Any

def check_default_cache_is_configured(
    app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any
) -> List[Error]: ...
