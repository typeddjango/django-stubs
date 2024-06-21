from collections.abc import Iterable
from datetime import date, datetime
from typing import Any, ClassVar, Literal, TypeVar, type_check_only

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager as BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.db.models.base import Model
from django.db.models.expressions import Combinable
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.db.models.manager import EmptyManager
from django.utils.functional import _StrOrPromise
from typing_extensions import Self, TypeAlias

_AnyUser: TypeAlias = Model | AnonymousUser

def update_last_login(sender: type[AbstractBaseUser], user: AbstractBaseUser, **kwargs: Any) -> None: ...

class PermissionManager(models.Manager[Permission]):
    def get_by_natural_key(self, codename: str, app_label: str, model: str) -> Permission: ...

class Permission(models.Model):
    objects: ClassVar[PermissionManager]

    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    name: models.CharField[str | int | Combinable, str]
    content_type: models.ForeignKey[ContentType | Combinable, ContentType]
    content_type_id: int
    codename: models.CharField[str | int | Combinable, str]
    group_set: ManyToManyDescriptor[Group, Group_permissions]
    def natural_key(self) -> tuple[str, str, str]: ...

class GroupManager(models.Manager[Group]):
    def get_by_natural_key(self, name: str) -> Group: ...

# This is a model that only exists in Django's model registry and doesn't have any
# class statement form. It's the through model between 'Group' and 'Permission'.
@type_check_only
class Group_permissions(models.Model):
    objects: ClassVar[models.Manager[Self]]

    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    group: models.ForeignKey[Group | Combinable, Group]
    group_id: int
    permission: models.ForeignKey[Permission | Combinable, Permission]
    permission_id: int

class Group(models.Model):
    objects: ClassVar[GroupManager]

    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]
    name: models.CharField[str | int | Combinable, str]
    permissions: models.ManyToManyField[Permission, Group_permissions]
    def natural_key(self) -> tuple[str]: ...

_T = TypeVar("_T", bound=Model)

class UserManager(BaseUserManager[_T]):
    def create_user(
        self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any
    ) -> _T: ...
    def create_superuser(
        self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any
    ) -> _T: ...
    def with_perm(
        self,
        perm: str | Permission,
        is_active: bool = ...,
        include_superusers: bool = ...,
        backend: str | None = ...,
        obj: Model | None = ...,
    ) -> QuerySet[_T]: ...

class PermissionsMixin(models.Model):
    is_superuser: models.BooleanField[bool | Combinable, bool]
    groups: models.ManyToManyField[Group, Any]
    user_permissions: models.ManyToManyField[Permission, Any]

    def get_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_group_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def has_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    def has_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    def has_module_perms(self, app_label: str) -> bool: ...

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator: UnicodeUsernameValidator

    username: models.CharField[str | int | Combinable, str]
    first_name: models.CharField[str | int | Combinable, str]
    last_name: models.CharField[str | int | Combinable, str]
    email: models.EmailField[str | Combinable, str]
    is_staff: models.BooleanField[bool | Combinable, bool]
    is_active: models.BooleanField[bool | Combinable, bool]
    date_joined: models.DateTimeField[str | datetime | date | Combinable, datetime]

    objects: ClassVar[UserManager[Self]]

    EMAIL_FIELD: str
    USERNAME_FIELD: str

    def get_full_name(self) -> str: ...
    def get_short_name(self) -> str: ...
    def email_user(
        self, subject: _StrOrPromise, message: _StrOrPromise, from_email: str = ..., **kwargs: Any
    ) -> None: ...

class User(AbstractUser):
    id: models.AutoField[str | int | Combinable | None, int]
    pk: models.AutoField[str | int | Combinable | None, int]

class AnonymousUser:
    id: Any
    pk: Any
    username: Literal[""]
    is_staff: Literal[False]
    is_active: Literal[False]
    is_superuser: Literal[False]
    def save(self) -> None: ...
    def delete(self) -> None: ...
    def set_password(self, raw_password: str) -> None: ...
    def check_password(self, raw_password: str) -> Any: ...
    @property
    def groups(self) -> EmptyManager[Group]: ...
    @property
    def user_permissions(self) -> EmptyManager[Permission]: ...
    def get_user_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def get_group_permissions(self, obj: _AnyUser | None = ...) -> set[Any]: ...
    def get_all_permissions(self, obj: _AnyUser | None = ...) -> set[str]: ...
    def has_perm(self, perm: str, obj: _AnyUser | None = ...) -> bool: ...
    def has_perms(self, perm_list: Iterable[str], obj: _AnyUser | None = ...) -> bool: ...
    def has_module_perms(self, module: str) -> bool: ...
    @property
    def is_anonymous(self) -> Literal[True]: ...
    @property
    def is_authenticated(self) -> Literal[False]: ...
    def get_username(self) -> str: ...
