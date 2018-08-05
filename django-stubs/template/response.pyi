from http.cookies import SimpleCookie
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from django.http import HttpResponse
from django.http.request import HttpRequest
from django.template.backends.django import Template
from django.template.backends.jinja2 import Template
from django.utils.safestring import SafeText

from .loader import get_template, select_template


class ContentNotRenderedError(Exception): ...

class SimpleTemplateResponse(HttpResponse):
    closed: bool
    cookies: http.cookies.SimpleCookie
    status_code: int
    rendering_attrs: Any = ...
    template_name: Union[
        str, django.template.backends.django.Template, List[str]
    ] = ...
    context_data: Optional[
        Union[Dict[str, str], Dict[str, Union[int, Callable]]]
    ] = ...
    using: Optional[str] = ...
    def __init__(
        self,
        template: Union[str, Template, List[str]],
        context: Any = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: None = ...,
        using: Optional[str] = ...,
    ) -> None: ...
    def resolve_template(
        self, template: Union[str, List[str]]
    ) -> Union[Template, Template]: ...
    def resolve_context(self, context: Any) -> Any: ...
    @property
    def rendered_content(self) -> SafeText: ...
    def add_post_render_callback(self, callback: Callable) -> None: ...
    content: Any = ...
    def render(self) -> TemplateResponse: ...
    @property
    def is_rendered(self) -> bool: ...
    def __iter__(self): ...
    @property
    def content(self): ...
    @content.setter
    def content(self, value: Any) -> None: ...

class TemplateResponse(SimpleTemplateResponse):
    client: django.test.client.Client
    closed: bool
    context: django.template.context.RequestContext
    context_data: Any
    cookies: http.cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, str]
    resolver_match: django.utils.functional.SimpleLazyObject
    status_code: int
    template_name: Union[
        str, django.template.backends.django.Template, List[str]
    ]
    templates: List[django.template.base.Template]
    using: Optional[str]
    wsgi_request: django.core.handlers.wsgi.WSGIRequest
    rendering_attrs: Any = ...
    def __init__(
        self,
        request: HttpRequest,
        template: Union[str, Template, List[str]],
        context: Any = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: None = ...,
        using: Optional[str] = ...,
    ) -> None: ...
