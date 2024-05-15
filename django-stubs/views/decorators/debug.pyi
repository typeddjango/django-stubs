from collections.abc import Callable
from typing import Literal

from . import _ViewFuncT

coroutine_functions_to_sensitive_variables: dict[int, Literal["__ALL__"] | tuple[str, ...]]

def sensitive_variables(*variables: str) -> Callable[[_ViewFuncT], _ViewFuncT]: ...
def sensitive_post_parameters(*parameters: str) -> Callable[[_ViewFuncT], _ViewFuncT]: ...
