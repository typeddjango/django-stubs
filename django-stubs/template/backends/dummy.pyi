import string
from typing import Any, Dict, List, Optional, Union, Tuple

from django.http.request import HttpRequest

from .base import BaseEngine

class TemplateStrings(BaseEngine):
    app_dirs: bool
    dirs: List[Any]
    name: str
    template_dirs: Tuple[str]
    app_dirname: str = ...
    def __init__(self, params: Dict[str, Union[Dict[Any, Any], List[Any], bool, str]]) -> None: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...

class Template(string.Template):
    template: str
    def render(self, context: Optional[Dict[str, str]] = ..., request: Optional[HttpRequest] = ...) -> str: ...
