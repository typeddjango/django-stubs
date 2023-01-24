from collections.abc import Callable
from typing import Any, TypeVar

from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.http.request import HttpRequest
from django.template.response import TemplateResponse

_C = TypeVar("_C", bound=Callable[..., Any])

def x_robots_tag(func: _C) -> _C: ...
def index(
    request: HttpRequest,
    sitemaps: dict[str, type[Sitemap[Any]] | Sitemap[Any]],
    template_name: str = ...,
    content_type: str = ...,
    sitemap_url_name: str = ...,
) -> TemplateResponse: ...
def sitemap(
    request: HttpRequest,
    sitemaps: dict[str, type[Sitemap[Any]] | Sitemap[Any]],
    section: str | None = ...,
    template_name: str = ...,
    content_type: str = ...,
) -> TemplateResponse: ...
