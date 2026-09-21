"""Reverse accessors are read from model instances, so a manager typed there must stay reachable."""

from __future__ import annotations

from typing import assert_type

from django.db import models
from django.db.models import manager

from django_stubs_ext.db.models.manager import RelatedManager

from .objects import Category, CategoryManager


class Article(models.Model):
    category_set: RelatedManager[Category]  # pyright: ignore[reportUninitializedInstanceVariable]
    loosely_typed_category_set: models.Manager[Category]  # pyright: ignore[reportUninitializedInstanceVariable]
    custom_category_set: CategoryManager  # pyright: ignore[reportUninitializedInstanceVariable]


class Node(models.Model):
    children: models.Manager[Node]  # pyright: ignore[reportUninitializedInstanceVariable]


def related_manager_access_on_instance_is_allowed() -> None:
    assert_type(Article().category_set, RelatedManager[Category])


def manager_of_another_model_on_instance_is_allowed() -> None:
    # pyrefly and ty don't hold the self-type of `BaseManager.__get__` to the receiver
    # TODO: drop the ignores once https://github.com/astral-sh/ty/issues/2799 is fixed and pyrefly follows
    assert_type(Article().loosely_typed_category_set, models.Manager[Category])  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(Article().custom_category_set, CategoryManager)  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]


def self_referential_manager_access_on_instance_is_banned() -> None:
    # Indistinguishable from `Node().objects`, annotate it as `RelatedManager[Node]` instead
    assert_type(Node().children, manager._ManagerIsNotAccessibleViaInstances)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]
