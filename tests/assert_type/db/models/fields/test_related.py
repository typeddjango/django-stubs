from __future__ import annotations

from typing import assert_type

from django.db import models


class Author(models.Model):
    pass


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, swappable=False)


class Profile(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE, swappable=False)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DB_CASCADE)
    author = models.OneToOneField(Author, on_delete=models.DB_SET_NULL)


def single_type_arg_is_also_the_get_type(fk: models.ForeignKey[Author], book: Book) -> None:
    assert_type(fk.__get__(book, Book), Author)
