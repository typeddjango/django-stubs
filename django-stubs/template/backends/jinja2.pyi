from collections.abc import Callable
from typing import Any

from django.template.exceptions import TemplateSyntaxError

from .base import BaseEngine

class Jinja2(BaseEngine):
    env: Any
    context_processors: list[str]
    def __init__(self, params: dict[str, Any]) -> None: ...
    @property
    def template_context_processors(self) -> list[Callable]: ...

class Origin:
    name: str
    template_name: str | None
    def __init__(self, name: str, template_name: str | None) -> None: ...

def get_exception_info(exception: TemplateSyntaxError) -> dict[str, Any]: ...
