# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class MyUser(models.Model):
    name = models.CharField(max_length=100)


def if_field_called_on_class_return_field_itself() -> None:
    # Class-level access yields a ``_FieldDescriptor`` exposing the field via ``.field``.
    assert_type(MyUser.name.field, "models.CharField[str | int | models.expressions.Combinable, str]")  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute, assert-type]  # ty: ignore[type-assertion-failure]
