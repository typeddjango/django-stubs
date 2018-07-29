from django.http.request import HttpRequest
from typing import (
    Dict,
    Optional,
    Union,
)


class Template:
    def render(
        self,
        context: Optional[Dict[str, str]] = ...,
        request: Optional[HttpRequest] = ...
    ) -> str: ...


class TemplateStrings:
    def __init__(self, params: Dict[str, Union[bool, str]]) -> None: ...
    def get_template(self, template_name: str) -> Template: ...