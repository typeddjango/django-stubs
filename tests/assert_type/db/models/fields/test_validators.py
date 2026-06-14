from collections.abc import Callable
from datetime import date
from decimal import Decimal

from django.db import models
from django.db.models.expressions import Combinable
from typing_extensions import assert_type


def validate_title(value: str) -> None: ...


def validate_price(value: Decimal) -> None: ...


def validate_published_on(value: date) -> None: ...


title_field: models.CharField[str | int | Combinable, str] = models.CharField(
    max_length=200,
    validators=[validate_title],
)
price_field: models.DecimalField[str | float | Decimal | Combinable, Decimal] = models.DecimalField(
    max_digits=8,
    decimal_places=2,
    validators=[validate_price],
)
published_on_field: models.DateField[str | date | Combinable, date] = models.DateField(
    validators=[validate_published_on],
)


assert_type(title_field.validators, list[Callable[[str], None]])  # ty: ignore[type-assertion-failure]
assert_type(price_field.validators, list[Callable[[Decimal], None]])  # ty: ignore[type-assertion-failure]
assert_type(published_on_field.validators, list[Callable[[date], None]])  # ty: ignore[type-assertion-failure]
