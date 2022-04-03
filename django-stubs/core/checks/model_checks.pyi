from typing import Any, Optional, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage

def check_all_models(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> Sequence[CheckMessage]: ...
def check_lazy_references(
    app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any
) -> Sequence[CheckMessage]: ...
