"""`objects` is reachable on the model class, never on an instance of that model."""

from __future__ import annotations

from typing import assert_type

from django.db import models
from django.db.models import manager


class CategoryManager(models.Manager["Category"]):
    pass


class Category(models.Model):
    objects = CategoryManager()
    secondary = CategoryManager()


class Post(models.Model):
    """No declared manager, `objects` only resolves through `ModelBase.__getattr__`."""


def declared_manager_access_on_instance_is_banned() -> None:
    assert_type(Category().objects, manager._ManagerIsNotAccessibleViaInstances)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]
    assert_type(Category().secondary, manager._ManagerIsNotAccessibleViaInstances)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]


def default_manager_access_on_instance_is_banned() -> None:
    # `ModelBase.__getattr__` lives on the metaclass, so instances can't reach it. mypy sees the
    # per-model attribute the plugin declares instead, and rejects it through `BaseManager.__get__`
    Post().objects  # type: ignore[deprecated]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


def manager_access_on_class_is_allowed() -> None:
    assert_type(Category.objects, CategoryManager)
    assert_type(Category.secondary, CategoryManager)
    assert_type(Post.objects, models.Manager[Post])


def unknown_attribute_is_still_an_error() -> None:
    # `Literal["objects"]` must not turn `__getattr__` into a catch-all
    Category.not_defined  # type: ignore[attr-defined]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-attribute-access]
    Category().not_defined  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


def meta_manager_access_on_instance_is_allowed() -> None:
    assert_type(Category()._meta.base_manager, models.Manager[Category])
    assert_type(Category()._meta.default_manager, models.Manager[Category] | None)
