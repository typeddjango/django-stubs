from datetime import datetime
from http.cookies import SimpleCookie
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from unittest.mock import MagicMock

from django.db.models.base import Model
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.template.backends.django import Template
from django.template.backends.jinja2 import Template
from django.views.generic.base import TemplateResponseMixin

from .loader import get_template as get_template, select_template as select_template


class ContentNotRenderedError(Exception): ...

class SimpleTemplateResponse(HttpResponse):
    closed: bool
    cookies: SimpleCookie
    status_code: int
    rendering_attrs: Any = ...
    template_name: Union[
        List[str], Template, str
    ] = ...
    context_data: Optional[Dict[str, str]] = ...
    using: Optional[str] = ...
    def __init__(
        self,
        template: Union[List[str], Template, str],
        context: Optional[Dict[str, Any]] = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: Optional[str] = ...,
        using: Optional[str] = ...,
    ) -> None: ...
    def resolve_template(
        self, template: Union[List[str], Template, str]
    ) -> Union[Template, Template]: ...
    def resolve_context(
        self,
        context: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]: ...
    @property
    def rendered_content(self) -> str: ...
    def add_post_render_callback(self, callback: Callable) -> None: ...
    content: Any = ...
    def render(self) -> SimpleTemplateResponse: ...
    @property
    def is_rendered(self) -> bool: ...
    def __iter__(self) -> Any: ...
    @property
    def content(self): ...
    @content.setter
    def content(self, value: Any) -> None: ...

class TemplateResponse(SimpleTemplateResponse):
    client: django.test.client.Client
    closed: bool
    context: django.template.context.RequestContext
    context_data: Optional[Dict[str, Any]]
    cookies: SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, Union[django.test.client.FakePayload, int, str]]
    resolver_match: django.utils.functional.SimpleLazyObject
    status_code: int
    template_name: Union[
        List[str], django.template.backends.django.Template, str
    ]
    templates: List[django.template.base.Template]
    using: Optional[str]
    wsgi_request: django.core.handlers.wsgi.WSGIRequest
    rendering_attrs: Any = ...
    def __init__(
        self,
        request: HttpRequest,
        template: Union[List[str], Template, str],
        context: Optional[
            Union[
                Dict[
                    str, List[Dict[str, Optional[Union[datetime, Model, str]]]]
                ],
                Dict[str, List[str]],
                Dict[str, Model],
                Dict[str, TemplateResponseMixin],
                Dict[str, str],
                MagicMock,
            ]
        ] = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: None = ...,
        using: Optional[str] = ...,
    ) -> None: ...
