from django.contrib.sites.models import Site
from django.db import models
from django.db.models.expressions import Combinable

class Redirect(models.Model):
    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    site: models.ForeignKey[Site | Combinable, Site]
    site_id: int
    old_path: models.CharField[str | int | Combinable, str]
    new_path: models.CharField[str | int | Combinable, str]
