from typing import Any, ClassVar

from django.db import models
from django.http import HttpRequest

SITE_CACHE: Any

class Site(models.Model):
    domain: str
    name: str
    id: int

    objects: ClassVar[SiteManager]

    def natural_key(self) -> tuple[str]: ...

class SiteManager(models.Manager["Site"]):
    def get_current(self, request: HttpRequest | None = ...) -> Site: ...
    def clear_cache(self) -> None: ...
    def get_by_natural_key(self, domain: str) -> Site: ...

def clear_site_cache(sender: type[Site], **kwargs: Any) -> None: ...
