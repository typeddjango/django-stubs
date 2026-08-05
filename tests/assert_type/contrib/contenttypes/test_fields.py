from __future__ import annotations

from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey, GenericForeignKeyDescriptor
from django.contrib.contenttypes.models import ContentType
from django.db import models
from typing_extensions import assert_type


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


assert_type(TaggedItem().content_object, Any | None)
assert_type(TaggedItem.content_object, GenericForeignKeyDescriptor)
