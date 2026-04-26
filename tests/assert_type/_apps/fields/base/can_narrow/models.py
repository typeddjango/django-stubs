from __future__ import annotations

from typing import NewType, cast

from django.db import models
from typing_extensions import assert_type

Year = NewType("Year", int)


class Book(models.Model):
    published = cast("models.Field[Year, Year]", models.IntegerField())


def can_narrow_field_type() -> None:
    book = Book()
    assert_type(book.published, Year)
    book.published = 2006  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-assignment]
    book.published = Year(2006)
    assert_type(book.published, Year)

    def accepts_int(arg: int) -> None: ...

    accepts_int(book.published)
