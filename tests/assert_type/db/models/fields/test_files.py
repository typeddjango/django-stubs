from __future__ import annotations

from django.db import models
from django.db.models.fields.files import FieldFile, ImageFieldFile
from typing_extensions import assert_type


class MyModel(models.Model):
    file = models.FileField()
    image = models.ImageField()

    null_file = models.FileField(null=True)
    null_image = models.ImageField(null=True)


instance = MyModel()
assert_type(instance.file, FieldFile)  # pyrefly: ignore[assert-type]
assert_type(instance.image, ImageFieldFile)  # pyrefly: ignore[assert-type]
assert_type(instance.null_file, FieldFile | None)  # pyrefly: ignore[assert-type]
assert_type(instance.null_image, ImageFieldFile | None)  # pyrefly: ignore[assert-type]
