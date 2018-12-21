from typing import Any, List, Optional

from django.core.checks.messages import CheckMessage

from .management import _get_builtin_permissions

def check_user_model(app_configs: None = ..., **kwargs: Any) -> List[CheckMessage]: ...
def check_models_permissions(app_configs: None = ..., **kwargs: Any) -> List[Any]: ...
