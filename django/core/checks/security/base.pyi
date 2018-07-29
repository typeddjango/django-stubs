from django.core.checks.messages import Warning
from typing import (
    Any,
    List,
)


def _security_middleware() -> bool: ...


def _xframe_middleware() -> bool: ...


def check_content_type_nosniff(app_configs: None, **kwargs) -> List[Warning]: ...


def check_debug(app_configs: None, **kwargs) -> List[Any]: ...


def check_secret_key(app_configs: None, **kwargs) -> List[Warning]: ...


def check_security_middleware(app_configs: None, **kwargs) -> List[Warning]: ...


def check_ssl_redirect(app_configs: None, **kwargs) -> List[Warning]: ...


def check_sts(app_configs: None, **kwargs) -> List[Warning]: ...


def check_xframe_deny(app_configs: None, **kwargs) -> List[Warning]: ...


def check_xss_filter(app_configs: None, **kwargs) -> List[Warning]: ...