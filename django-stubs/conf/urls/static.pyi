from typing import Any

from django.urls.resolvers import URLPattern
from django.views import _ViewCallable

def static(prefix: str, view: _ViewCallable = ..., **kwargs: Any) -> list[URLPattern]: ...
