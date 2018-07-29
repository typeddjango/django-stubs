from django.core.checks.messages import Warning
from typing import List


def _csrf_middleware() -> bool: ...


def check_csrf_middleware(app_configs: None, **kwargs) -> List[Warning]: ...