from collections.abc import Callable, Sequence
from typing import Any, overload

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression, Combinable
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar

_ModelT = TypeVar("_ModelT", bound=Model)
_F = TypeVar("_F", bound=Callable[..., Any])

@overload
def action(
    function: _F,
    *,
    permissions: Sequence[str] | None = ...,
    description: _StrOrPromise | None = ...,
) -> _F: ...
@overload
def action(
    function: None = None,
    *,
    permissions: Sequence[str] | None = ...,
    description: _StrOrPromise | None = ...,
) -> Callable[[_F], _F]: ...
@overload
def display(
    function: _F,
    *,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: None = ...,
) -> _F: ...
@overload
def display(
    function: _F,
    *,
    boolean: None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: str | None = ...,
) -> _F: ...
@overload
def display(
    function: None = None,
    *,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: None = ...,
) -> Callable[[_F], _F]: ...
@overload
def display(
    *,
    boolean: None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: _StrOrPromise | None = ...,
    empty_value: str | None = ...,
) -> Callable[[_F], _F]: ...
def register(
    *models: type[_ModelT], site: AdminSite | None = ...
) -> Callable[[type[ModelAdmin[_ModelT]]], type[ModelAdmin[_ModelT]]]: ...
