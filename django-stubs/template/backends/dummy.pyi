import string
from typing import Any, Mapping

from django.http.request import HttpRequest
from django.template.context import _ContextKeys

from .base import BaseEngine

class TemplateStrings(BaseEngine):
    template_dirs: tuple[str]
    def __init__(self, params: dict[str, dict[Any, Any] | list[Any] | bool | str]) -> None: ...

class Template(string.Template):
    template: str
    def render(self, context: Mapping[_ContextKeys, Any] | None = ..., request: HttpRequest | None = ...) -> str: ...
