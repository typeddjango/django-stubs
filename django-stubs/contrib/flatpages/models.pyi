from typing import Any

from django.contrib.sites.models import Site
from django.db import models

class FlatPage(models.Model):
    url: models.CharField[Any, Any]
    title: models.CharField[Any, Any]
    content: models.TextField[Any, Any]
    enable_comments: models.BooleanField[Any, Any]
    template_name: models.CharField[Any, Any]
    registration_required: models.BooleanField[Any, Any]
    sites: models.ManyToManyField[Site, Site]
    def get_absolute_url(self) -> str: ...
