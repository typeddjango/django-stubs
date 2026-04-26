"""This case has no Django model — the file exists only to satisfy the per-case
``models.py`` convention. The test exercises ``IntegerField`` annotation on a
plain class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import assert_type

if TYPE_CHECKING:
    from django.db import models


class NonModel:
    myfield: models.IntegerField[int, int]  # pyright: ignore[reportUninitializedInstanceVariable]


def fields_on_non_model_classes_resolve_to_field_type() -> None:
    assert_type(NonModel.myfield, "models.fields._FieldDescriptor[models.IntegerField[int, int]]")  # pyrefly: ignore[assert-type]
    assert_type(NonModel.myfield.field, "models.IntegerField[int, int]")  # pyrefly: ignore[missing-attribute, assert-type]
    assert_type(NonModel().myfield, "models.IntegerField[int, int]")
