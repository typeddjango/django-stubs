from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

def sensitive_variables(*variables: Any) -> Callable[[_F], _F]: ...
def sensitive_post_parameters(*parameters: Any) -> Callable[[_F], _F]: ...
