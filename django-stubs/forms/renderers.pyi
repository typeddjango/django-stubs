from typing import Any

from django.http import HttpRequest
from django.template.backends.base import BaseEngine
from django.template.backends.django import DjangoTemplates as DjangoTemplatesR
from django.template.backends.jinja2 import Jinja2 as Jinja2R
from django.template.base import Template

def get_default_renderer() -> BaseRenderer: ...

class BaseRenderer:
    def get_template(self, template_name: str) -> Any: ...
    def render(self, template_name: str, context: dict[str, Any], request: HttpRequest | None = ...) -> str: ...

class EngineMixin:
    def get_template(self, template_name: str) -> Any: ...
    @property
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    backend: type[DjangoTemplatesR]

class Jinja2(EngineMixin, BaseRenderer):
    @property
    def backend(self) -> type[Jinja2R]: ...

class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template | None: ...
