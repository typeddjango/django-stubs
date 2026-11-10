from __future__ import annotations

from typing import Any, assert_type

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields import IntegerField, _FieldDescriptor


class MyClass:
    myfield: models.IntegerField[int, int]  # pyright: ignore[reportUninitializedInstanceVariable]


def fields_on_non_model_classes_resolve_to_field_type() -> None:
    assert_type(MyClass.myfield, _FieldDescriptor[IntegerField[int, int]])
    assert_type(MyClass.myfield.field, IntegerField[int, int])
    assert_type(MyClass().myfield, IntegerField[int, int])


def relation_fields_built_outside_a_model_class_keep_their_related_model() -> None:
    assert_type(models.ManyToManyField(ContentType), models.ManyToManyField[ContentType, Any])
    assert_type(GenericRelation(ContentType), GenericRelation[ContentType])
