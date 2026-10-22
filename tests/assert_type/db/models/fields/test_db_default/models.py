from __future__ import annotations

from typing import assert_type

from django.db import models


class Book(models.Model):
    pages = models.IntegerField(null=True, db_default=None)  # pyright: ignore[reportUnknownVariableType]


def db_default_does_not_narrow_set_type(book: Book) -> None:
    assert_type(book.pages, int | None)  # pyright: ignore[reportAssertTypeFailure,reportUnknownMemberType]  # ty: ignore[type-assertion-failure]
    book.pages = 1
