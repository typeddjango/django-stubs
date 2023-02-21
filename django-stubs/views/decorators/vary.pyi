from collections.abc import Callable
from typing import Any, TypeVar

from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_F = TypeVar("_F", bound=Callable[..., Any])

def vary_on_headers(*headers: Callable[_P, _F]) -> Callable[_P, _F]: ...
def vary_on_cookie(func: _F) -> _F: ...
