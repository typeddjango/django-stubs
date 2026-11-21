from __future__ import annotations

import sys
from typing import assert_type

from django.db import models


class Author(models.Model):
    pass


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, swappable=False)
    editor = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    sequel = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)


class Profile(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE, swappable=False)
    mentor = models.OneToOneField(Author, on_delete=models.SET_NULL, null=True)
    best_book = models.OneToOneField("test_related_forward.Book", on_delete=models.CASCADE)


# `DB_CASCADE`/`DB_SET_NULL` are only available in Django 6.1+ but we test against Django 5.2.x on Python < 3.12.
if sys.version_info >= (3, 12):

    class Review(models.Model):
        book = models.ForeignKey(Book, on_delete=models.DB_CASCADE)
        author = models.OneToOneField(Author, on_delete=models.DB_SET_NULL)


def test_related() -> None:
    assert_type(Book().author, Author)
    assert_type(Profile().user, Author)


def class_reference_with_null_true_is_optional() -> None:
    assert_type(Book().editor, Author | None)
    assert_type(Profile().mentor, Author | None)
    Book().editor = None
    Book().author = None  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]


def lazy_reference_is_only_resolved_by_django_aware_checkers() -> None:
    assert_type(Book().sequel, Book | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(Profile().best_book, Book)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


def non_literal_null_is_deprecated(flag: bool) -> None:
    models.ForeignKey(Author, on_delete=models.CASCADE, null=flag)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # pyrefly: ignore[deprecated]  # ty: ignore[deprecated]
    models.OneToOneField(Author, on_delete=models.CASCADE, null=flag)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # pyrefly: ignore[deprecated]  # ty: ignore[deprecated]


def single_type_arg_is_also_the_get_type(fk: models.ForeignKey[Author], book: Book) -> None:
    assert_type(fk.__get__(book, Book), Author)
