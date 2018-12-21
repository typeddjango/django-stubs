from typing import Optional

from django.contrib.sitemaps import Sitemap
from django.db.models.query import QuerySet

class FlatPageSitemap(Sitemap):
    def items(self) -> QuerySet: ...
