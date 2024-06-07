from typing import ClassVar, type_check_only

from django.contrib.sites.models import Site
from django.db import models
from django.db.models.expressions import Combinable
from typing_extensions import Self

# This is a model that only exists in Django's model registry and doesn't have any
# class statement form. It's the through model between 'FlatPage' and 'Site'.
@type_check_only
class FlatPage_sites(models.Model):
    objects: ClassVar[models.Manager[Self]]

    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    site: models.ForeignKey[Site | Combinable, Site]
    site_id: int
    flatpage: models.ForeignKey[FlatPage | Combinable, FlatPage]
    flatpage_id: int

class FlatPage(models.Model):
    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    url: models.CharField[str | int | Combinable, str]
    title: models.CharField[str | int | Combinable, str]
    content: models.TextField[str | int | Combinable, str]
    enable_comments: models.BooleanField[bool | Combinable, bool]
    template_name: models.CharField[str | int | Combinable, str]
    registration_required: models.BooleanField[bool | Combinable, bool]
    sites: models.ManyToManyField[Site, FlatPage_sites]
    def get_absolute_url(self) -> str: ...
