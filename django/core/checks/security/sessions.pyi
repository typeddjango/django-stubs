from typing import (
    Any,
    List,
)


def _session_app() -> bool: ...


def _session_middleware() -> bool: ...


def check_session_cookie_secure(app_configs: None, **kwargs) -> List[Any]: ...