"""Managers are only accessible on the model class, never on an instance."""

from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from django.contrib.auth.models import AnonymousUser, Group
from django.db import models
from django.db.models.manager import EmptyManager

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import RelatedManager


class CategoryManager(models.Manager["Category"]):
    pass


class Category(models.Model):
    objects = CategoryManager()
    secondary = CategoryManager()


class Post(models.Model):
    """No declared manager, `objects` only resolves through `ModelBase.__getattr__`."""


class Article(models.Model):
    # Reverse accessors are bound to instances, so they must be annotated with `RelatedManager`, not a bare `Manager`.
    category_set: RelatedManager[Category]  # pyright: ignore[reportUninitializedInstanceVariable]


def declared_manager_access_on_instance_is_banned() -> None:
    # ty doesn't check the `instance` argument of `__get__`, so it accepts both accesses
    Category().objects  # type: ignore[arg-type]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[bad-argument-type]
    Category().secondary  # type: ignore[arg-type]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[bad-argument-type]


def default_manager_access_on_instance_is_banned() -> None:
    # `ModelBase.__getattr__` lives on the metaclass, so instances can't reach it. mypy sees the
    # per-model attribute the plugin declares instead, and rejects it through `BaseManager.__get__`
    Post().objects  # type: ignore[arg-type]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


def manager_access_on_class_is_allowed() -> None:
    # A declared manager keeps its own type, exactly like any other class attribute
    assert_type(Category.objects, CategoryManager)
    assert_type(Category.secondary, CategoryManager)
    assert_type(Post.objects, models.Manager[Post])


def unknown_attribute_is_still_an_error() -> None:
    # `Literal["objects"]` must not turn `__getattr__` into a catch-all
    Category.not_defined  # type: ignore[attr-defined]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[unresolved-attribute]
    Category().not_defined  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


def related_manager_access_on_instance_is_allowed() -> None:
    assert_type(Article().category_set, "RelatedManager[Category]")


def empty_manager_access_through_property_is_allowed() -> None:
    # `EmptyManager` reaches instances through `AnonymousUser.groups`, a plain property
    assert_type(AnonymousUser().groups, EmptyManager[Group])


def meta_manager_access_on_instance_is_allowed() -> None:
    # `Options` hands out managers from an instance the same way
    assert_type(Category()._meta.base_manager, models.Manager[Category])
