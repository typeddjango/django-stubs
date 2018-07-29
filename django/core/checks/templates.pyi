from django.core.checks.messages import Error
from typing import (
    Any,
    List,
)


def check_setting_app_dirs_loaders(app_configs: None, **kwargs) -> List[Any]: ...


def check_string_if_invalid_is_string(app_configs: None, **kwargs) -> List[Error]: ...