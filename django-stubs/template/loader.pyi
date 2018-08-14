from typing import Dict, List, Optional, Union

from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template as DjangoTemplate
from django.template.backends.dummy import Template as DummyTemplate
from django.template.backends.jinja2 import Template as Jinja2Template


def get_template(
    template_name: str, using: Optional[str] = ...
) -> Union[DjangoTemplate, DummyTemplate, Jinja2Template]: ...
def select_template(
    template_name_list: Union[List[str], str], using: Optional[str] = ...
) -> Union[DjangoTemplate, DummyTemplate, Jinja2Template]: ...
def render_to_string(
    template_name: Union[List[str], str],
    context: Optional[Union[Dict[str, bool], Dict[str, str]]] = ...,
    request: Optional[WSGIRequest] = ...,
    using: Optional[str] = ...,
) -> str: ...
