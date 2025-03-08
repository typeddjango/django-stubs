from django.db import models

class Redirect(models.Model):
    # Note: do not create `class Meta` here.
    site: models.ForeignKey
    old_path: models.CharField
    new_path: models.CharField
