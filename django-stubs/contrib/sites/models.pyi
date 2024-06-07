from typing import Any, ClassVar

from django.contrib.flatpages.models import FlatPage, FlatPage_sites
from django.contrib.redirects.models import Redirect
from django.db import models
from django.db.models.expressions import Combinable
from django.db.models.fields.related_descriptors import ManyToManyDescriptor, ReverseManyToOneDescriptor
from django.http.request import HttpRequest

SITE_CACHE: Any

class SiteManager(models.Manager[Site]):
    def get_current(self, request: HttpRequest | None = ...) -> Site: ...
    def clear_cache(self) -> None: ...
    def get_by_natural_key(self, domain: str) -> Site: ...

class Site(models.Model):
    objects: ClassVar[SiteManager]

    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    domain: models.CharField[str | int | Combinable, str]
    name: models.CharField[str | int | Combinable, str]
    flatpage_set: ManyToManyDescriptor[FlatPage, FlatPage_sites]
    redirect_set: ReverseManyToOneDescriptor[Redirect]
    def natural_key(self) -> tuple[str]: ...

def clear_site_cache(sender: type[Site], **kwargs: Any) -> None: ...
