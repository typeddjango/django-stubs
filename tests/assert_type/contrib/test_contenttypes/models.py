from __future__ import annotations

import sys
from typing import Any, assert_type

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# `GenericForeignKeyDescriptor` is only available in Django 6.1+ but we test against Django 5.2.x
# on Python < 3.12, so only run these tests for newer Python versions to avoid lots of issues with
# different type checkers complaining when attempting to fall back to `GenericForeignKey`
# when `ImportError` is raised.
if sys.version_info >= (3, 12):
    from django.contrib.contenttypes.fields import GenericForeignKeyDescriptor

    class TaggedItem(models.Model):
        tag = models.SlugField()  # pyright: ignore[reportUnknownVariableType]
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # pyright: ignore[reportUnknownVariableType]
        object_id = models.PositiveBigIntegerField()  # pyright: ignore[reportUnknownVariableType]
        content_object = GenericForeignKey("content_type", "object_id")

    def test_generic_foreign_key_descriptor() -> None:
        assert_type(TaggedItem().content_object, Any | None)  # pyrefly: ignore[assert-type]
        assert_type(TaggedItem.content_object, GenericForeignKeyDescriptor)  # pyrefly: ignore[assert-type]
