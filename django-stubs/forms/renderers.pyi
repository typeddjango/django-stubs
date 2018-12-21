from typing import Any, Dict, Union

import django.template.backends as template_backends
from django.template import Template
from django.template.backends.base import BaseEngine

ROOT: Any

def get_default_renderer() -> DjangoTemplates: ...

class BaseRenderer:
    def get_template(self, template_name: str) -> Any: ...
    def render(self, template_name: str, context: Dict[str, Any], request: None = ...) -> str: ...

class EngineMixin:
    def get_template(
        self, template_name: str
    ) -> Union[template_backends.django.Template, template_backends.jinja2.Template]: ...
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    engine: template_backends.django.DjangoTemplates
    backend: Any = ...

class Jinja2(EngineMixin, BaseRenderer):
    engine: template_backends.jinja2.Jinja2
    backend: Any = ...

class TemplatesSetting(BaseRenderer):
    def get_template(self, template_name: str) -> Template: ...
