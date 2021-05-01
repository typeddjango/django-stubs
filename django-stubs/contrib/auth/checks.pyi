from typing import Any, List, Optional, Sequence

from django.core.checks.messages import CheckMessage

from django.apps.config import AppConfig

def check_user_model(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[CheckMessage]: ...
def check_models_permissions(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[CheckMessage]: ...
