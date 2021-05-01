from typing import Any, List, Optional, Sequence

from django.core.checks.messages import CheckMessage, Warning

from django.apps.config import AppConfig

def check_all_models(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[CheckMessage]: ...
def check_lazy_references(app_configs: Optional[Sequence[AppConfig]] = ..., **kwargs: Any) -> List[CheckMessage]: ...
