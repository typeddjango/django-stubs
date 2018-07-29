from django.contrib.sitemaps import Sitemap
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
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
    sitemaps: Dict[str, Any],
    section: Optional[str] = ...,
    template_name: str = ...,
    content_type: str = ...
) -> TemplateResponse: ...


def x_robots_tag(func: Callable) -> Callable: ...