# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class MyModel(models.Model):
    nulltext = models.CharField(max_length=1, blank=True, null=True)


def blank_and_null_char_field_allows_none() -> None:
    MyModel(nulltext="")
    MyModel(nulltext=None)
    MyModel().nulltext = None
    assert_type(MyModel().nulltext, "str | None")  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
