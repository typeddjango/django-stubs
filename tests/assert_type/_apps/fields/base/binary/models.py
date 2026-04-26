# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class EncodedMessage(models.Model):
    message = models.BinaryField()


def test_binary_field_return_types() -> None:
    assert_type(EncodedMessage(message=b"\x010").message, "bytes | memoryview[int]")  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
