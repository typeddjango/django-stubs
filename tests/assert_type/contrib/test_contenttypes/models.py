from __future__ import annotations

from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey, GenericForeignKeyDescriptor
from django.contrib.contenttypes.models import ContentType
from django.db import models
from typing_extensions import assert_type


class TaggedItem(models.Model):
    tag = models.SlugField()  # pyright: ignore[reportUnknownVariableType]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # pyright: ignore[reportUnknownVariableType]
    object_id = models.PositiveBigIntegerField()  # pyright: ignore[reportUnknownVariableType]
    content_object = GenericForeignKey("content_type", "object_id")


def test_generic_foreign_key_descriptor() -> None:
    assert_type(TaggedItem().content_object, Any | None)  # pyrefly: ignore[assert-type]
    assert_type(TaggedItem.content_object, GenericForeignKeyDescriptor)  # pyrefly: ignore[assert-type]
