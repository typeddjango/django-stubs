from typing import Any, List, Optional

from django.core.checks.messages import Error

E001: Any
E002: Any

def check_setting_app_dirs_loaders(app_configs: None, **kwargs: Any) -> List[Error]: ...
def check_string_if_invalid_is_string(app_configs: None, **kwargs: Any) -> List[Error]: ...
