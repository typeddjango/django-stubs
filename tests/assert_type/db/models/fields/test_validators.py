from collections.abc import Callable
from datetime import date
from decimal import Decimal
from typing import NewType
from uuid import UUID

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


SlugValue = NewType("SlugValue", str)


class CustomSlugField(models.SlugField[SlugValue | str | int | Combinable, SlugValue]): ...


def validate_slug(value: str) -> None: ...


def validate_identifier(value: UUID) -> None: ...


def validate_ip(value: str) -> None: ...


def validate_custom_slug(value: SlugValue) -> None: ...


def validate_int(value: int) -> None: ...


# Only the mypy plugin resolves these field types, and so only mypy rejects the `bad_*` validators.
class Article(models.Model):
    slug = models.SlugField(validators=[validate_slug])  # pyright: ignore[reportUnknownVariableType]
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[validate_price])  # pyright: ignore[reportUnknownVariableType]
    published_on = models.DateField(validators=[validate_published_on])  # pyright: ignore[reportUnknownVariableType]
    identifier = models.UUIDField(validators=[validate_identifier])  # pyright: ignore[reportUnknownVariableType]
    ip_address = models.GenericIPAddressField(validators=[validate_ip])  # pyright: ignore[reportUnknownVariableType]
    custom_slug = CustomSlugField(validators=[validate_custom_slug])

    bad_slug = models.SlugField(validators=[validate_int])  # type: ignore[list-item]  # pyright: ignore[reportUnknownVariableType]
    bad_published_on = models.DateField(validators=[validate_int])  # type: ignore[list-item]  # pyright: ignore[reportUnknownVariableType]
    bad_identifier = models.UUIDField(validators=[validate_published_on])  # type: ignore[list-item]  # pyright: ignore[reportUnknownVariableType]
    bad_ip_address = models.GenericIPAddressField(validators=[validate_identifier])  # type: ignore[list-item]  # pyright: ignore[reportUnknownVariableType]
    bad_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[validate_identifier])  # type: ignore[list-item]  # pyright: ignore[reportUnknownVariableType]


assert_type(Article().slug, str)  # ty: ignore[type-assertion-failure]
assert_type(Article().price, Decimal)  # ty: ignore[type-assertion-failure]
assert_type(Article().published_on, date)  # ty: ignore[type-assertion-failure]
assert_type(Article().identifier, UUID)  # ty: ignore[type-assertion-failure]
assert_type(Article().ip_address, str)  # ty: ignore[type-assertion-failure]
assert_type(Article().custom_slug, SlugValue)  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
