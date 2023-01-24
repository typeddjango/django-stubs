from typing import Any

from django.db import models

class Redirect(models.Model):
    site: models.ForeignKey[Any, Any]
    old_path: models.CharField[Any, Any]
    new_path: models.CharField[Any, Any]
