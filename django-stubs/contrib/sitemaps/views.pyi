from collections import OrderedDict
from typing import Any, Callable, Dict, Optional, Type, Union

from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse

def x_robots_tag(func: Callable) -> Callable: ...
def index(
    request: WSGIRequest,
    sitemaps: Dict[str, Union[Type[Sitemap], Sitemap]],
    template_name: str = ...,
    content_type: str = ...,
    sitemap_url_name: str = ...,
) -> TemplateResponse: ...
def sitemap(
    request: WSGIRequest,
    sitemaps: Union[Dict[str, Type[Sitemap]], Dict[str, GenericSitemap], OrderedDict],
    section: Optional[str] = ...,
    template_name: str = ...,
    content_type: str = ...,
) -> TemplateResponse: ...
