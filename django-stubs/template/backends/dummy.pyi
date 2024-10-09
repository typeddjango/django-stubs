import string
from typing import Any

from django.http.request import HttpRequest

from .base import BaseEngine

class TemplateStrings(BaseEngine):
    def __init__(self, params: dict[str, dict[Any, Any] | list[Any] | bool | str]) -> None: ...

class Template(string.Template):
    template: str
    def render(self, context: dict[str, Any] | None = ..., request: HttpRequest | None = ...) -> str: ...
