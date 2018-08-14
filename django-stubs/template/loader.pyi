from typing import Any, Dict, List, Optional, Union

from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template
from django.template.backends.dummy import Template
from django.template.backends.jinja2 import Template

from .exceptions import TemplateDoesNotExist


def get_template(
    template_name: str, using: Optional[str] = ...
) -> Union[Template, Template, Template]: ...
def select_template(
    template_name_list: Union[List[str], str], using: Optional[str] = ...
) -> Union[Template, Template, Template]: ...
def render_to_string(
    template_name: Union[List[str], str],
    context: Optional[Union[Dict[str, bool], Dict[str, str]]] = ...,
    request: Optional[WSGIRequest] = ...,
    using: Optional[str] = ...,
) -> str: ...
