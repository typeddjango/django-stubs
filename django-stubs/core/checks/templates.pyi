from collections.abc import Sequence
from typing import Any

from django.apps.config import AppConfig
from django.core.checks.messages import Error

E001: Error
E002: Error

def check_setting_app_dirs_loaders(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> Sequence[Error]: ...
def check_string_if_invalid_is_string(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> Sequence[Error]: ...
