from typing import Any

from django.forms.boundfield import BoundField
from django.http import HttpRequest
from django.template.backends.base import BaseEngine, _EngineTemplate
from django.template.backends.django import DjangoTemplates as DjangoTemplatesR
from django.template.backends.django import Template as DjangoTemplate
from django.template.backends.jinja2 import Jinja2 as Jinja2R
from django.template.backends.jinja2 import Template as Jinja2Template
from django.utils.functional import cached_property
from typing_extensions import override

def get_default_renderer() -> BaseRenderer: ...

class BaseRenderer:
    form_template_name: str
    formset_template_name: str
    field_template_name: str
    bound_field_class: type[BoundField] | None
    def get_template(self, template_name: str) -> _EngineTemplate: ...
    def render(self, template_name: str, context: dict[str, Any], request: HttpRequest | None = None) -> str: ...

class EngineMixin:
    def get_template(self, template_name: str) -> _EngineTemplate: ...
    @cached_property
    def engine(self) -> BaseEngine: ...

class DjangoTemplates(EngineMixin, BaseRenderer):
    backend: type[DjangoTemplatesR]
    @override
    def get_template(self, template_name: str) -> DjangoTemplate: ...
    @override
    @cached_property
    def engine(self) -> DjangoTemplatesR: ...

class Jinja2(EngineMixin, BaseRenderer):
    @cached_property
    def backend(self) -> type[Jinja2R]: ...
    @override
    def get_template(self, template_name: str) -> Jinja2Template: ...
    @override
    @cached_property
    def engine(self) -> Jinja2R: ...

class TemplatesSetting(BaseRenderer):
    @override
    def get_template(self, template_name: str) -> _EngineTemplate: ...
