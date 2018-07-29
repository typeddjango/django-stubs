from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    AnonymousUser,
    User,
)
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.options import Options
from django.http.request import HttpRequest
from django.utils.functional import SimpleLazyObject
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)


def _clean_credentials(credentials: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]: ...


def _get_backends(return_tuples: bool = ...) -> Any: ...


def _get_user_session_key(request: HttpRequest) -> int: ...


def authenticate(
    request: Optional[HttpRequest] = ...,
    **credentials
) -> Optional[AbstractBaseUser]: ...


def get_backends() -> List[ModelBackend]: ...


def get_permission_codename(action: str, opts: Options) -> str: ...


def get_user(
    request: HttpRequest
) -> Union[AnonymousUser, AbstractBaseUser]: ...


def get_user_model() -> Type[Model]: ...


def load_backend(path: str) -> object: ...


def login(
    request: HttpRequest,
    user: User,
    backend: Optional[Union[str, Type[ModelBackend]]] = ...
) -> None: ...


def logout(request: HttpRequest) -> None: ...


def update_session_auth_hash(
    request: WSGIRequest,
    user: SimpleLazyObject
) -> None: ...