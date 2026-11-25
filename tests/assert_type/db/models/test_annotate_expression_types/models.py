from __future__ import annotations

import datetime
from typing import assert_type

from django.db import models
from django.db.models import DateTimeField, IntegerField, Max, Sum


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published = models.DateTimeField()


# pyright and ty don't type `annotate()` attributes. pyrefly types them as `Any` whatever the
# expression: https://github.com/pyrefly-org/pyrefly/issues/5734


def output_field_decides_the_attribute_type() -> None:
    author = Author.objects.annotate(
        total=Sum("books__price", output_field=IntegerField()),
        latest=Max("books__published", output_field=DateTimeField()),
        null_total=Sum("books__price", output_field=IntegerField(null=True)),
    ).get()
    assert_type(author.total, int | None)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]
    assert_type(author.latest, datetime.datetime | None)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]
    assert_type(author.null_total, int | None)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]


def default_makes_the_attribute_non_nullable() -> None:
    author = Author.objects.annotate(
        total=Sum("books__price", output_field=IntegerField(), default=0),
        explicit_none=Sum("books__price", output_field=IntegerField(), default=None),
        null_total=Sum("books__price", output_field=IntegerField(null=True), default=0),
    ).get()
    assert_type(author.total, int)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]
    assert_type(author.explicit_none, int | None)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]
    # a nullable output field stays nullable
    assert_type(author.null_total, int | None)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[missing-attribute, type-assertion-failure]
