from collections.abc import Callable, Sequence
from typing import Any, TypeVar, Union, overload  # noqa: Y037

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import Combinable, QuerySet
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression
from django.http import HttpRequest, HttpResponseBase
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeAlias

_Model = TypeVar("_Model", bound=Model)
_ModelAdmin = TypeVar("_ModelAdmin", bound=ModelAdmin)
_Request = TypeVar("_Request", bound=HttpRequest)
_QuerySet = TypeVar("_QuerySet", bound=QuerySet)
# This is deliberately different from _DisplayT defined in contrib.admin.options
_DisplayCallable: TypeAlias = Union[Callable[[_ModelAdmin, _Model], Any], Callable[[_Model], Any]]  # noqa: Y037
_DisplayCallableT = TypeVar("_DisplayCallableT", bound=_DisplayCallable)
_ActionReturn = TypeVar("_ActionReturn", bound=HttpResponseBase | None)

@overload
def action(
    function: Callable[[_ModelAdmin, _Request, _QuerySet], _ActionReturn],
    permissions: Sequence[str] | None = ...,
    description: _StrOrPromise | None = ...,
) -> Callable[[_ModelAdmin, _Request, _QuerySet], _ActionReturn]: ...
@overload
def action(
    *,
    permissions: Sequence[str] | None = ...,
    description: _StrOrPromise | None = ...,
) -> Callable[
    [Callable[[_ModelAdmin, _Request, _QuerySet], _ActionReturn]],
    Callable[[_ModelAdmin, _Request, _QuerySet], _ActionReturn],
]: ...
@overload
def display(
    function: _DisplayCallableT,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: str | None = ...,
) -> _DisplayCallableT: ...
@overload
def display(
    *,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: str | None = ...,
) -> Callable[[_DisplayCallableT], _DisplayCallableT]: ...
def register(
    *models: type[Model], site: AdminSite | None = ...
) -> Callable[[type[_ModelAdmin]], type[_ModelAdmin]]: ...
