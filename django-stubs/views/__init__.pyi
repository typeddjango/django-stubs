from collections.abc import Callable, Coroutine
from typing import Any, TypeAlias

from django.http.response import HttpResponseBase
from typing_extensions import TypeVar

from .generic.base import View as View

_AsyncViewCallable: TypeAlias = Callable[..., Coroutine[Any, Any, HttpResponseBase]]  # ruff: ignore[unused-private-type-alias]
_ViewCallable: TypeAlias = Callable[..., HttpResponseBase]
_ViewCallableT = TypeVar("_ViewCallableT", bound=_ViewCallable)  # ruff: ignore[unused-private-type-var]

__all__ = ["View"]
