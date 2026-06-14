from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class Author(models.Model):
    pass


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, swappable=False)


class Profile(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE, swappable=False)


def test_related() -> None:
    assert_type(Book().author, Author)  # ty: ignore[type-assertion-failure] # pyright: ignore[reportAssertTypeFailure]
    assert_type(Profile().user, Author)  # ty: ignore[type-assertion-failure] # pyright: ignore[reportAssertTypeFailure]
