from collections.abc import Callable, Sequence
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

def csp_override(config: dict[str, Sequence[str] | str]) -> Callable[[_F], _F]: ...
def csp_report_only_override(config: dict[str, Sequence[str] | str]) -> Callable[[_F], _F]: ...
