from django.contrib.sites.models import Site
from django.db import models

class FlatPage(models.Model):
    url: models.CharField[str | int, str]
    title: models.CharField[str | int, str]
    content: models.TextField[str, str]
    enable_comments: models.BooleanField[bool, bool]
    template_name: models.CharField[str | int, str]
    registration_required: models.BooleanField[bool, bool]
    sites = models.ManyToManyField(Site)
    def get_absolute_url(self) -> str: ...
