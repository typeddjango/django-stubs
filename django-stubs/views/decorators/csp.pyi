from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

def csp_override(config: dict[str, Any]) -> Callable[[_F], _F]: ...
def csp_report_only_override(config: dict[str, Any]) -> Callable[[_F], _F]: ...
