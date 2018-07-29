from django.template.backends.django import (
    DjangoTemplates,
    Template,
)
from typing import (
    Any,
    Dict,
)


def get_default_renderer() -> DjangoTemplates: ...


class BaseRenderer:
    def render(self, template_name: str, context: Dict[str, Any], request: None = ...) -> str: ...


class EngineMixin:
    @cached_property
    def engine(self) -> DjangoTemplates: ...
    def get_template(self, template_name: str) -> Template: ...