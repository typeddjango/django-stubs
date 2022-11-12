from typing import Any, Callable, Sequence, Type, TypeVar

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import Combinable, QuerySet
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression
from django.http import HttpRequest

_ModelT = TypeVar("_ModelT", bound=Model)

def action(
    function: Callable[[ModelAdmin, HttpRequest, QuerySet], None] | None = ...,
    *,
    permissions: Sequence[str] | None = ...,
    description: str | None = ...,
) -> Callable: ...
def display(
    function: Callable[[_ModelT], Any] | None = ...,
    *,
    boolean: bool | None = ...,
    ordering: str | Combinable | BaseExpression | None = ...,
    description: str | None = ...,
    empty_value: str | None = ...,
) -> Callable: ...
def register(*models: Type[Model], site: AdminSite | None = ...) -> Callable: ...
