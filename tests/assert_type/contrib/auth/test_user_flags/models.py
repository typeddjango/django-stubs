from __future__ import annotations

from typing import Literal, Never, assert_type

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, AnonymousUser, PermissionsMixin, User
from django.db import models
from django.db.models import F, Value
from typing_extensions import override


class MyUser(AbstractUser):
    pass


class NullableActiveUser(AbstractUser):
    is_active = models.BooleanField(null=True)  # type: ignore[assignment]  # pyrefly: ignore[bad-override-mutable-attribute]


class PropertyStaffUser(AbstractUser):
    @property
    @override
    def is_staff(self) -> Literal[True]:  # type: ignore[override]  # pyright: ignore[reportIncompatibleVariableOverride]  # pyrefly: ignore[bad-override]  # ty: ignore[invalid-property-type-override]
        return True


def overridden_flags_keep_their_declared_type() -> None:
    # pyright and ty don't apply `null=True` yet: https://github.com/typeddjango/django-stubs/pull/3317
    assert_type(NullableActiveUser().is_active, bool | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(PropertyStaffUser().is_staff, Literal[True])


def flags_accept_expressions(user: User) -> None:
    # pyrefly types field assignments without `Combinable`: https://github.com/facebook/pyrefly/issues/5322
    user.is_active = F("is_staff")  # pyrefly: ignore[bad-assignment]
    user.is_staff = Value(True)  # pyrefly: ignore[bad-assignment]


class MyBaseUser(AbstractBaseUser, PermissionsMixin):
    # pyright rejects the bases' distinct `Meta` classes unless the model inherits both,
    # ty wrongly rejects that override: https://github.com/astral-sh/ty/issues/4711
    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):  # ty: ignore[invalid-attribute-override]
        pass


def abstract_user_subclass_flags_are_bool() -> None:
    user = MyUser()
    assert_type(user.is_staff, bool)
    assert_type(user.is_active, bool)
    assert_type(user.is_superuser, bool)


def abstract_base_user_with_permissions_mixin_flags_are_bool() -> None:
    user = MyBaseUser()
    assert_type(user.is_active, bool)
    assert_type(user.is_superuser, bool)


def user_is_authenticated(user: User) -> None:
    assert_type(user.is_authenticated, Literal[True])


def anonymous_user_flags_are_false(user: AnonymousUser) -> None:
    assert_type(user.is_staff, Literal[False])
    assert_type(user.is_active, Literal[False])
    assert_type(user.is_superuser, Literal[False])
    assert_type(user.is_authenticated, Literal[False])


# Regression test for https://github.com/typeddjango/django-stubs/issues/512
def user_or_anonymous_user_flags_are_bool(user: User | AnonymousUser) -> None:
    assert_type(user.is_staff, bool)
    assert_type(user.is_active, bool)
    assert_type(user.is_superuser, bool)
    assert_type(user.is_authenticated, bool)


def anonymous_user_has_no_db_representation(user: AnonymousUser) -> None:
    assert_type(user.check_password("x"), Never)


def user_or_anonymous_user_methods(user: User | AnonymousUser) -> None:
    assert_type(user.check_password("x"), bool)
    assert_type(user.get_group_permissions(), set[str])
