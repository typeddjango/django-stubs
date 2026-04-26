# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class MyModel(models.Model):
    small = models.SmallAutoField(primary_key=True)


def test_small_auto_field_class_presents_as_int() -> None:
    assert_type(MyModel().small, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
