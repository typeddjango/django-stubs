from django.contrib.sites.models import Site
from django.db import models

class Redirect(models.Model):
    site: models.ForeignKey[Site]
    old_path: models.CharField[str]
    new_path: models.CharField[str]
