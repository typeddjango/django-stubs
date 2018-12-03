from typing import Any, List, Optional

from django.core.checks.messages import Warning

W003: Any
W016: Any

def check_csrf_middleware(app_configs: None, **kwargs: Any) -> List[Warning]: ...
def check_csrf_cookie_secure(app_configs: None, **kwargs: Any) -> List[Warning]: ...
