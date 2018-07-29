from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import (
    GenericSitemap,
    Sitemap,
)
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from typing import (
    Callable,
    Dict,
    Optional,
    Type,
    Union,
)


def index(
    request: WSGIRequest,
    sitemaps: Dict[str, Type[Sitemap]],
    template_name: str = ...,
    content_type: str = ...,
    sitemap_url_name: str = ...
) -> TemplateResponse: ...


def sitemap(
    request: WSGIRequest,
    sitemaps: Dict[str, Union[Type[Sitemap], Type[FlatPageSitemap], GenericSitemap]],
    section: Optional[str] = ...,
    template_name: str = ...,
    content_type: str = ...
) -> TemplateResponse: ...


def x_robots_tag(func: Callable) -> Callable: ...