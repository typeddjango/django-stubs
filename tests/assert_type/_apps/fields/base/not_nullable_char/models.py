# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class MyModel(models.Model):
    notnulltext = models.CharField(max_length=1, blank=True, null=False)


def blank_and_not_null_charfield_does_not_allow_none() -> None:
    MyModel(notnulltext=None)  # type: ignore[misc]
    MyModel(notnulltext="")
    MyModel().notnulltext = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]
    assert_type(MyModel().notnulltext, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
