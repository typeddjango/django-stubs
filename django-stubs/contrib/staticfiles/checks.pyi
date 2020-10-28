from typing import Any, List, Optional, Sequence

from django.core.checks.messages import Error

from django.apps.config import AppConfig

def check_finders(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[Error]: ...
