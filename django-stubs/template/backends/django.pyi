from django.http.request import HttpRequest
from django.template.base import Template
from django.template.exceptions import TemplateDoesNotExist
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    Iterator,
    Optional,
)


def copy_exception(
    exc: TemplateDoesNotExist,
    backend: Optional[DjangoTemplates] = ...
) -> TemplateDoesNotExist: ...


def get_installed_libraries() -> Dict[str, str]: ...


def get_package_libraries(pkg: Any) -> Iterator[str]: ...


def reraise(
    exc: TemplateDoesNotExist,
    backend: DjangoTemplates
): ...


class DjangoTemplates:
    def __init__(self, params: Dict[str, Any]) -> None: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...
    def get_templatetag_libraries(self, custom_libraries: Dict[str, str]) -> Dict[str, str]: ...


class Template:
    def __init__(
        self,
        template: Template,
        backend: DjangoTemplates
    ) -> None: ...
    def render(
        self,
        context: Any = ...,
        request: Optional[HttpRequest] = ...
    ) -> SafeText: ...