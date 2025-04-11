from typing import Any, ClassVar

from django.contrib.flatpages.models import FlatPage, _FlatPage_sites
from django.contrib.redirects.models import Redirect
from django.db import models
from django.db.models.fields.related_descriptors import ManyToManyDescriptor, ReverseManyToOneDescriptor
from django.http.request import HttpRequest

SITE_CACHE: Any

class SiteManager(models.Manager[Site]):
    def get_current(self, request: HttpRequest | None = ...) -> Site: ...
    def clear_cache(self) -> None: ...
    def get_by_natural_key(self, domain: str) -> Site: ...

class Site(models.Model):
    objects: ClassVar[SiteManager]

    id: models.AutoField
    pk: models.AutoField
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    flatpage_set: ManyToManyDescriptor[FlatPage, _FlatPage_sites]
    redirect_set: ReverseManyToOneDescriptor[Redirect]
    def natural_key(self) -> tuple[str]: ...

def clear_site_cache(sender: type[Site], **kwargs: Any) -> None: ...
