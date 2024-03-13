from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

coroutine_functions_to_sensitive_variables: dict[int, str | tuple[str, ...]]

def sensitive_variables(*variables: str) -> Callable[[_F], _F]: ...
def sensitive_post_parameters(*parameters: str) -> Callable[[_F], _F]: ...
