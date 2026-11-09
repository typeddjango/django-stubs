from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, assert_type

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation, ReverseGenericManyToOneDescriptor
from django.contrib.contenttypes.models import ContentType
from django.db import models

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import RelatedManager

# `GenericForeignKeyDescriptor` is only available in Django 6.1+ but we test against Django 5.2.x
# on Python < 3.12, so only run these tests for newer Python versions to avoid lots of issues with
# different type checkers complaining when attempting to fall back to `GenericForeignKey`
# when `ImportError` is raised.
if sys.version_info >= (3, 12):
    from django.contrib.contenttypes.fields import GenericForeignKeyDescriptor

    class TaggedItem(models.Model):
        tag = models.SlugField()
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveBigIntegerField()
        content_object = GenericForeignKey("content_type", "object_id")

    def test_generic_foreign_key_descriptor() -> None:
        assert_type(TaggedItem().content_object, Any | None)  # pyrefly: ignore[assert-type]
        assert_type(TaggedItem.content_object, GenericForeignKeyDescriptor)  # pyrefly: ignore[assert-type]

    class Bookmark(models.Model):
        tags = GenericRelation(TaggedItem)

    # Django imports this module at runtime, where the stub-only `RelatedManager` doesn't exist.
    if TYPE_CHECKING:

        def test_generic_relation() -> None:
            # pyrefly resolves fields from the class and ignores `__get__`: https://github.com/meta/pyrefly/issues/5532
            assert_type(Bookmark().tags, RelatedManager[TaggedItem])  # pyrefly: ignore[assert-type]
            assert_type(Bookmark.tags, ReverseGenericManyToOneDescriptor[TaggedItem])  # pyrefly: ignore[assert-type]
