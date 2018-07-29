from django.urls.resolvers import URLPattern
from typing import (
    Callable,
    List,
)


def static(prefix: str, view: Callable = ..., **kwargs) -> List[URLPattern]: ...