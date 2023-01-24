from collections.abc import Callable
from typing import Any

from django.urls.resolvers import URLPattern

def static(prefix: str, view: Callable[..., Any] = ..., **kwargs: Any) -> list[URLPattern]: ...
