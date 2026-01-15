from django.db import models
from django.db.models.fields.files import FieldFile, ImageFieldFile
from typing_extensions import assert_type


class MyModel(models.Model):
    file = models.FileField()
    image = models.ImageField()


instance = MyModel()
assert_type(instance.file, FieldFile)  # pyrefly: ignore[assert-type]
assert_type(instance.image, ImageFieldFile)  # pyrefly: ignore[assert-type]
