from __future__ import annotations

from django.db import models


class Book(models.Model):
    pages = models.IntegerField(null=True, db_default=None)  # pyright: ignore[reportUnknownVariableType]


def db_default_does_not_narrow_set_type(book: Book) -> None:
    book.pages = 1
