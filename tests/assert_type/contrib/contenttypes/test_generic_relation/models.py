from __future__ import annotations

from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from typing_extensions import assert_type


class TaggedItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Bookmark(models.Model):
    tags = GenericRelation(TaggedItem)


def test_generic_relation() -> None:
    assert_type(Bookmark().tags, Any)
