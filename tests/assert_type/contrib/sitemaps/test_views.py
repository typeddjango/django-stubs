from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import index, sitemap

if TYPE_CHECKING:
    from django.http.request import HttpRequest


class BlogSitemap(Sitemap[str]): ...


def sitemap_views(request: HttpRequest) -> None:
    # Inferred as `dict[str, BlogSitemap]`, only accepted by a covariant `Mapping`
    sitemaps = {"blog": BlogSitemap()}
    index(request, sitemaps)
    sitemap(request, sitemaps, section="blog")
