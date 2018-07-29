from django.http.request import HttpRequest
from django.template.backends.django import Template
from django.utils.safestring import SafeText
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


class SimpleTemplateResponse:
    def __getstate__(self) -> Dict[str, Any]: ...
    def __init__(
        self,
        template: Union[str, List[str], Template],
        context: Any = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: Optional[str] = ...,
        using: None = ...
    ) -> None: ...
    def add_post_render_callback(self, callback: Callable) -> None: ...
    @property
    def is_rendered(self) -> bool: ...
    def render(self) -> SimpleTemplateResponse: ...
    @property
    def rendered_content(self) -> SafeText: ...
    def resolve_context(self, context: Any) -> Any: ...
    def resolve_template(
        self,
        template: Union[str, List[str], Template]
    ) -> Template: ...


class TemplateResponse:
    def __init__(
        self,
        request: HttpRequest,
        template: Union[str, List[str], Template],
        context: Any = ...,
        content_type: Optional[str] = ...,
        status: Optional[int] = ...,
        charset: None = ...,
        using: None = ...
    ) -> None: ...