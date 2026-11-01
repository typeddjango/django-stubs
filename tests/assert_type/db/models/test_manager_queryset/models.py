"""The queryset type param of managers: declared with `Manager[Model, QuerySet]` or defaulted from the model."""

from __future__ import annotations

import datetime
import uuid
from typing import assert_type

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from typing_extensions import override

# ---------------------------------------------------------------------------
# Declared queryset param: `Manager[Model, QuerySet]` flows through every chainable method
# ---------------------------------------------------------------------------


class BlogQuerySet(models.QuerySet["Blog"]):
    def queryset_method(self) -> int:
        return 0


class OtherBlogQuerySet(models.QuerySet["Blog"]): ...


class BlogManager(models.Manager["Blog", BlogQuerySet]):
    @override
    def get_queryset(self) -> BlogQuerySet:
        return BlogQuerySet(self.model, using=self._db)


class ConflictingBlogManager(models.Manager["Blog", BlogQuerySet]):
    # `get_queryset` has to return the declared queryset param
    @override
    def get_queryset(self) -> OtherBlogQuerySet:  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-method-override]
        return OtherBlogQuerySet(self.model, using=self._db)


class Blog(models.Model):
    created_at = models.DateTimeField()
    objects = BlogManager()
    conflicting = ConflictingBlogManager()


def manager_methods_return_the_declared_queryset_type_param() -> None:
    assert_type(Blog.objects, BlogManager)
    assert_type(Blog.objects.get_queryset(), BlogQuerySet)
    assert_type(Blog.objects.all(), BlogQuerySet)
    assert_type(Blog.objects.filter(), BlogQuerySet)
    assert_type(Blog.objects.only("id"), BlogQuerySet)
    assert_type(Blog.objects.union(Blog.objects.all()), BlogQuerySet)
    assert_type(Blog.objects.all().queryset_method(), int)
    assert_type(Blog.objects.get(), Blog)
    # Methods building a differently-typed queryset stay plain `QuerySet`
    assert_type(Blog.objects.dates("created_at", "day"), QuerySet[Blog, datetime.date])


def custom_queryset_methods_return_self(qs: BlogQuerySet) -> None:
    assert_type(qs[:9], BlogQuerySet)
    assert_type(qs.none(), BlogQuerySet)
    assert_type(qs & qs, BlogQuerySet)
    assert_type(qs.get(), Blog)


# ---------------------------------------------------------------------------
# The default `objects` manager is inherited with the subclass as model
# Regression test for https://github.com/typeddjango/django-stubs/issues/1023
# ---------------------------------------------------------------------------


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class ConcreteChild(UUIDModel):
    name = models.CharField(max_length=100)


class UUIDAbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractChild(UUIDAbstractModel):
    pass


class AbstractChildRelated(UUIDAbstractModel):
    child = models.ForeignKey(AbstractChild, on_delete=models.CASCADE)


def inherited_default_objects_manager() -> None:
    assert_type(UUIDModel.objects, models.Manager[UUIDModel])
    assert_type(ConcreteChild.objects, models.Manager[ConcreteChild])
    assert_type(AbstractChild.objects, models.Manager[AbstractChild])
    assert_type(AbstractChildRelated.objects, models.Manager[AbstractChildRelated])
    assert_type(ConcreteChild.objects.all(), QuerySet[ConcreteChild])


# ---------------------------------------------------------------------------
# A direct `BaseManager` subclass is a valid manager
# ---------------------------------------------------------------------------


class RawManager(BaseManager["RawModel"]):
    pass


class RawModel(models.Model):
    objects = RawManager()


def base_manager_direct_subclass() -> None:
    assert_type(RawModel.objects, RawManager)
    assert_type(RawModel.objects.get_queryset(), QuerySet[RawModel])


# ---------------------------------------------------------------------------
# A custom manager method is inherited along with the manager
# Regression test for https://github.com/typeddjango/django-stubs/issues/1067#issuecomment-1216350505
# ---------------------------------------------------------------------------


class TenantUserManager(BaseUserManager):  # pyright: ignore[reportMissingTypeArgument]
    def create_user(self, email: str | None = None, password: str | None = None, is_staff: bool = False) -> None: ...


class PermissionsMixinFacade: ...


class TenantUser(AbstractBaseUser, PermissionsMixinFacade):
    objects = TenantUserManager()


class SiteUser(TenantUser):
    pass


def inherited_custom_manager_method() -> None:
    SiteUser.objects.create_user("foo@mail.com", "password", is_staff=True)
    SiteUser.objects.create_user("foo@mail.com", "password", is_staff=12)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
