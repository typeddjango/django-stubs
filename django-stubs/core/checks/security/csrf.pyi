from typing import Any, Optional, Sequence

from django.apps.config import AppConfig
from django.core.checks.messages import Warning

W003: Warning
W016: Warning

def check_csrf_middleware(app_configs: Optional[Sequence[AppConfig]], **kwargs: Any) -> Sequence[Warning]: ...
def check_csrf_cookie_secure(app_configs: Optional[Sequence[AppConfig]], **kwargs: Any) -> Sequence[Warning]: ...
