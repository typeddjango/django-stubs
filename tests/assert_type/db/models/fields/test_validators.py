from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal


def validate_title(value: str) -> None: ...
def validate_price(value: Decimal) -> None: ...
def validate_published_on(value: date) -> None: ...
def validate_int(value: int) -> None: ...


class Author(models.Model): ...


class Article(models.Model):
    title = models.CharField(max_length=200, validators=[validate_title])
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[validate_price])
    # Validators never see `None`, `Field.run_validators()` skips empty values.
    published_on = models.DateField(null=True, validators=[validate_published_on])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, validators=[validate_int])

    bad_title = models.CharField(max_length=200, validators=[validate_int])  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-argument-type]
    bad_published_on = models.DateField(null=True, validators=[validate_int])  # type: ignore[list-item]  # pyright: ignore[reportCallIssue, reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
