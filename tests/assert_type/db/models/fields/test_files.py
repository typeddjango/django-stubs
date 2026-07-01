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
# At runtime, FileDescriptor.__get__ ALWAYS returns a FieldFile even when the underlying database value is NULL.
# It wraps None in FieldFile(instance, field, name=None).
# For ex:
# In [4]: Page.objects.get(video__isnull=False).video
# Out[4]: <FieldFile: video-1280x720_Pw9M7ro.webm>
#
# In [5]: Page.objects.get(video__isnull=True).video
# Out[5]: <FieldFile: None>

assert_type(instance.file, FieldFile)
assert_type(instance.image, ImageFieldFile)
assert_type(instance.null_file, FieldFile)
assert_type(instance.null_image, ImageFieldFile)
