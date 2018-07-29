from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    AnonymousUser,
    User,
)
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from typing import (
    Optional,
    Set,
    Union,
)


class AllowAllUsersModelBackend:
    def user_can_authenticate(self, user: User) -> bool: ...


class AllowAllUsersRemoteUserBackend:
    def user_can_authenticate(self, user: User) -> bool: ...


class ModelBackend:
    def _get_group_permissions(self, user_obj: User) -> QuerySet: ...
    def _get_permissions(self, user_obj: User, obj: None, from_name: str) -> Set[str]: ...
    def _get_user_permissions(self, user_obj: User) -> QuerySet: ...
    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = ...,
        password: Optional[str] = ...,
        **kwargs
    ) -> Optional[User]: ...
    def get_all_permissions(self, user_obj: User, obj: Optional[str] = ...) -> Set[str]: ...
    def get_group_permissions(self, user_obj: User, obj: None = ...) -> Set[str]: ...
    def get_user(self, user_id: int) -> User: ...
    def get_user_permissions(self, user_obj: User, obj: None = ...) -> Set[str]: ...
    def has_module_perms(
        self,
        user_obj: Union[AnonymousUser, User],
        app_label: str
    ) -> bool: ...
    def has_perm(
        self,
        user_obj: Union[AnonymousUser, User],
        perm: str,
        obj: None = ...
    ) -> bool: ...
    def user_can_authenticate(self, user: Optional[AbstractBaseUser]) -> bool: ...


class RemoteUserBackend:
    def authenticate(
        self,
        request: WSGIRequest,
        remote_user: Optional[str]
    ) -> Optional[User]: ...
    def clean_username(self, username: str) -> str: ...
    def configure_user(self, user: User) -> User: ...