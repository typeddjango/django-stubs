# pyright: reportUnknownVariableType=none
from __future__ import annotations

from decimal import Decimal

from django.contrib.postgres import fields as pg_fields
from django.db import models
from typing_extensions import assert_type


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    time_range = pg_fields.DateTimeRangeField(null=False)
    some_decimal = models.DecimalField(max_digits=10, decimal_places=5)


def test_model_field_classes_from_existing_locations() -> None:
    booking = Booking()
    assert_type(booking.id, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    # DateTimeRangeField has no specific stub typing and resolves to Any.
    booking.time_range
    assert_type(booking.some_decimal, Decimal)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
