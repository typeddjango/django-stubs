from django.contrib.sites.models import Site
from django.db import models

class Redirect(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    old_path = models.CharField(max_length=200)
    new_path = models.CharField(max_length=200, blank=True)
