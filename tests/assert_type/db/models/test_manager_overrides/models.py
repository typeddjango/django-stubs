"""Overriding `Manager.create()` with a narrowed return type.

Regression test for https://github.com/typeddjango/django-stubs/issues/578.
"""

from __future__ import annotations

from typing import Any, assert_type

from django.db import models
from typing_extensions import override

# ---------------------------------------------------------------------------
# Unparametrized manager: the plugin re-parametrizes it with the model it's on
# ---------------------------------------------------------------------------


class ArticleManager(models.Manager):  # pyright: ignore[reportMissingTypeArgument]
    # Without a type parameter, the inherited `create()` returns the unsolved `_T`, so narrowing it is an error.
    # Only mypy checks the override against `_T`, the other type checkers treat it as unknown.
    @override
    def create(self, **kwargs: Any) -> Article:  # type: ignore[override]
        return super().create(**kwargs)  # type: ignore[return-value]  # pyright: ignore[reportUnknownVariableType]


class Article(models.Model):
    objects = ArticleManager()


def override_manager_create_no_type_param() -> None:
    assert_type(Article.objects.create(), Article)


# ---------------------------------------------------------------------------
# Manager parametrized with the model it's assigned to
# ---------------------------------------------------------------------------


class BookManager(models.Manager["Book"]):
    @override
    def create(self, **kwargs: Any) -> Book:
        return super().create(**kwargs)


class Book(models.Model):
    objects = BookManager()


def override_manager_create_with_type_param() -> None:
    assert_type(Book.objects.create(), Book)


# ---------------------------------------------------------------------------
# Manager parametrized with another model than the one it's assigned to
# ---------------------------------------------------------------------------


class ReviewManager(models.Manager["Author"]):
    # The type parameter, not the model the manager ends up on, drives what the inherited `create()` returns.
    @override
    def create(self, **kwargs: Any) -> Review:  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-method-override]
        return super().create(**kwargs)  # type: ignore[return-value]  # pyright: ignore[reportReturnType]  # pyrefly: ignore[bad-return]  # ty: ignore[invalid-return-type]


class Review(models.Model):
    objects = ReviewManager()  # pyright: ignore[reportGeneralTypeIssues]


class Author(models.Model):
    pass


def override_manager_create_with_incoherent_type_param() -> None:
    assert_type(Review.objects.create(), Review)
