from typing import Callable, Dict, Optional, Type, TypeVar, Union

from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.http.request import HttpRequest
from django.template.response import TemplateResponse

_C = TypeVar("_C", bound=Callable)

def x_robots_tag(func: _C) -> _C: ...
def index(
    request: HttpRequest,
    sitemaps: Dict[str, Union[Type[Sitemap], Sitemap]],
    template_name: str = ...,
    content_type: str = ...,
    sitemap_url_name: str = ...,
) -> TemplateResponse: ...
def sitemap(
    request: HttpRequest,
    sitemaps: Dict[str, Union[Type[Sitemap], Sitemap]],
    section: Optional[str] = ...,
    template_name: str = ...,
    content_type: str = ...,
) -> TemplateResponse: ...
