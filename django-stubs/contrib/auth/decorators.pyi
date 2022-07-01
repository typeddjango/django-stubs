from typing import Callable, Iterable, Optional, TypeVar, Union, overload

from django.contrib.auth import REDIRECT_FIELD_NAME as REDIRECT_FIELD_NAME  # noqa: F401
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http.response import HttpResponseBase

_VIEW = TypeVar("_VIEW", bound=Callable[..., HttpResponseBase])

def user_passes_test(
    test_func: Callable[[Union[AbstractBaseUser, AnonymousUser]], bool],
    login_url: Optional[str] = ...,
    redirect_field_name: str = ...,
) -> Callable[[_VIEW], _VIEW]: ...

# There are two ways of calling @login_required: @with(arguments) and @bare
@overload
def login_required(redirect_field_name: str = ..., login_url: Optional[str] = ...) -> Callable[[_VIEW], _VIEW]: ...
@overload
def login_required(function: _VIEW, redirect_field_name: str = ..., login_url: Optional[str] = ...) -> _VIEW: ...
def permission_required(
    perm: Union[Iterable[str], str], login_url: Optional[str] = ..., raise_exception: bool = ...
) -> Callable[[_VIEW], _VIEW]: ...
