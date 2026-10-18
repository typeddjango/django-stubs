"""Managers are only accessible on the model class, never on an instance of that model."""

from __future__ import annotations

from typing import Generic, Protocol, assert_type

from django.contrib.auth.models import AnonymousUser, Group
from django.db import models
from django.db.models import manager
from django.db.models.manager import EmptyManager
from typing_extensions import TypeVar

from django_stubs_ext.db.models.manager import RelatedManager


class CategoryManager(models.Manager["Category"]):
    pass


class Category(models.Model):
    objects = CategoryManager()
    secondary = CategoryManager()


class Post(models.Model):
    """No declared manager, `objects` only resolves through `ModelBase.__getattr__`."""


class Article(models.Model):
    category_set: RelatedManager[Category]  # pyright: ignore[reportUninitializedInstanceVariable]
    loosely_typed_category_set: models.Manager[Category]  # pyright: ignore[reportUninitializedInstanceVariable]
    custom_category_set: CategoryManager  # pyright: ignore[reportUninitializedInstanceVariable]


class Node(models.Model):
    children: models.Manager[Node]  # pyright: ignore[reportUninitializedInstanceVariable]


_MT_co = TypeVar("_MT_co", bound=models.Model, covariant=True)


class QuerySetHolder(Generic[_MT_co]):
    """Plain classes hold managers too, this mirrors DRF's `GenericAPIView.queryset`."""

    queryset: models.Manager[_MT_co] | models.QuerySet[_MT_co] | None = None


class CategoryHolder(QuerySetHolder[Category]):
    def assign(self) -> None:
        self.queryset = Category.objects.all()


class UnparametrizedHolder(QuerySetHolder):  # pyright: ignore[reportMissingTypeArgument]
    queryset = Category.objects


class PermissionAware(Protocol):
    groups: models.Manager[Group]


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


def related_manager_access_on_instance_is_allowed() -> None:
    assert_type(Article().category_set, RelatedManager[Category])


def manager_of_another_model_on_instance_is_allowed() -> None:
    assert_type(Article().loosely_typed_category_set, models.Manager[Category])
    assert_type(Article().custom_category_set, CategoryManager)


def self_referential_manager_access_on_instance_is_banned() -> None:
    # Indistinguishable from `Node().objects`, annotate it as `RelatedManager[Node]` instead
    assert_type(Node().children, manager._ManagerIsNotAccessibleViaInstances)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[type-assertion-failure]


def manager_on_plain_class_is_allowed() -> None:
    assert_type(CategoryHolder().queryset, models.Manager[Category] | models.QuerySet[Category] | None)
    UnparametrizedHolder().queryset  # pyright: ignore[reportUnknownMemberType]


def manager_on_protocol_is_allowed(user: PermissionAware) -> None:
    assert_type(user.groups, models.Manager[Group])


def empty_manager_access_through_property_is_allowed() -> None:
    # `EmptyManager` reaches instances through `AnonymousUser.groups`, a plain property
    assert_type(AnonymousUser().groups, EmptyManager[Group])
