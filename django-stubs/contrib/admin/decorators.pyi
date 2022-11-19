from collections.abc import Callable, Sequence
from typing import Any, TypeVar, overload

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import Combinable, QuerySet
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression
from django.http import HttpRequest
from django.utils.functional import _StrPromise

_T = TypeVar("_T")
_Model = TypeVar("_Model", bound=Model)
_ModelAdmin = TypeVar("_ModelAdmin", bound=ModelAdmin)
_Request = TypeVar("_Request", bound=HttpRequest)
_QuerySet = TypeVar("_QuerySet", bound=QuerySet)

@overload
def action(
    function: Callable[[_ModelAdmin, _Request, _QuerySet], None],
    permissions: Sequence[str] | None = ...,
    description: _StrPromise | None = ...,
) -> Callable[[_ModelAdmin, _Request, _QuerySet], None]: ...
@overload
def action(
    *,
    permissions: Sequence[str] | None = ...,
    description: _StrPromise | None = ...,
) -> Callable[
    [Callable[[_ModelAdmin, _Request, _QuerySet], None]], Callable[[_ModelAdmin, _Request, _QuerySet], None]
]: ...
@overload
def display(
    function: Callable[[_Model], _T],
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrPromise | None = ...,
    empty_value: str | None = ...,
) -> Callable[[_Model], _T]: ...
@overload
def display(
    *,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrPromise | None = ...,
    empty_value: str | None = ...,
) -> Callable[[Callable[[_Model], _T]], Callable[[_Model], _T]]: ...
def register(
    *models: type[Model], site: AdminSite | None = ...
) -> Callable[[type[_ModelAdmin]], type[_ModelAdmin]]: ...
