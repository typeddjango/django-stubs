from typing import Any, Dict

from django.template import Template
from django.template.backends.base import BaseEngine

ROOT: Any

def get_default_renderer() -> DjangoTemplates: ...

class BaseRenderer:
    def get_template(self, template_name: str) -> Any: ...
    def render(self, template_name: str, context: Dict[str, Any], request: None = ...) -> str: ...

class EngineMixin:
    def get_template(self, template_name: str) -> Any: ...
    @property
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    backend: Any = ...

class Jinja2(EngineMixin, BaseRenderer):
    @property
    def backend(self) -> Type[Jinja2R]: ...

class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template: ...
