from typing import Any, Optional, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage

def check_user_model(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> Sequence[CheckMessage]: ...
def check_models_permissions(
    app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any
) -> Sequence[CheckMessage]: ...
