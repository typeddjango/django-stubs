from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from django.db.models.fields import IntegerField, _FieldDescriptor

if TYPE_CHECKING:
    from django.db import models


class MyClass:
    myfield: models.IntegerField[int, int]  # pyright: ignore[reportUninitializedInstanceVariable]


def fields_on_non_model_classes_resolve_to_field_type() -> None:
    assert_type(MyClass.myfield, _FieldDescriptor[IntegerField[int, int]])
    assert_type(MyClass.myfield.field, IntegerField[int, int])
    assert_type(MyClass().myfield, IntegerField[int, int])
