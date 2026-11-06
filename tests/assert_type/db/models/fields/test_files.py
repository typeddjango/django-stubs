from __future__ import annotations

from typing import assert_type

from django.core.files.storage import Storage
from django.db import models
from django.db.models.fields.files import FieldFile, FileDescriptor, ImageFieldFile, ImageFileDescriptor


class MyModel(models.Model):
    file = models.FileField()
    image = models.ImageField()

    null_file = models.FileField(null=True)
    null_image = models.ImageField(null=True)


instance = MyModel()
# `FileDescriptor.__get__` always returns a `FieldFile`, even for a NULL value,
# which is wrapped as `FieldFile(instance, field, name=None)`.
assert_type(instance.file, FieldFile)
assert_type(instance.image, ImageFieldFile)
assert_type(instance.null_file, FieldFile)
assert_type(instance.null_image, ImageFieldFile)


def image_field_accepts_file_field_kwargs() -> None:
    # ImageField forwards `upload_to`/`storage` to FileField at runtime, so both must type-check.
    class WithKwargs(models.Model):
        avatar = models.ImageField(upload_to="avatars/")
        cover = models.ImageField(upload_to="covers/", storage=Storage())

    instance = WithKwargs()
    assert_type(instance.avatar, ImageFieldFile)
    assert_type(instance.cover, ImageFieldFile)


def file_and_image_class_access_returns_specific_descriptor() -> None:
    # Class-level access returns the field's own descriptor, not a generic `_FieldDescriptor`.
    class WithFiles(models.Model):
        doc = models.FileField()
        pic = models.ImageField()

    assert_type(WithFiles.doc, FileDescriptor)
    assert_type(WithFiles.pic, ImageFileDescriptor)
