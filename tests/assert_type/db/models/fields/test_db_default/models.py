from __future__ import annotations

from typing import assert_type

from django.db import models


class Book(models.Model):
    pages = models.IntegerField(null=True, db_default=None)
    chapters = models.IntegerField(db_default=1)


def db_default_does_not_narrow_set_type(book: Book) -> None:
    assert_type(book.pages, int | None)
    book.pages = 1
    assert_type(book.chapters, int)
    book.chapters = "1"
