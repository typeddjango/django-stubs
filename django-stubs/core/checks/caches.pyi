from typing import Any, Optional, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import Error, Warning

E001: Error

def check_default_cache_is_configured(app_configs: Optional[Sequence[AppConfig]], **kwargs: Any) -> Sequence[Error]: ...
def check_cache_location_not_exposed(
    app_configs: Optional[Sequence[AppConfig]], **kwargs: Any
) -> Sequence[Warning]: ...
def check_file_based_cache_is_absolute(
    app_configs: Optional[Sequence[AppConfig]], **kwargs: Any
) -> Sequence[Warning]: ...
