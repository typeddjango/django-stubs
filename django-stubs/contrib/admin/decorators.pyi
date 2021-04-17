from typing import Callable, Optional, Type, Sequence, Union, TypeVar, Any

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import Combinable, QuerySet
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression
from django.http import HttpRequest

_ModelT = TypeVar("_ModelT", bound=Model)

def action(
    function: Optional[Callable[[ModelAdmin, HttpRequest, QuerySet], None]] = ...,
    *,
    permissions: Optional[Sequence[str]] = ...,
    description: Optional[str] = ...,
) -> Callable: ...
def display(
    function: Optional[Callable[[_ModelT], Any]] = ...,
    *,
    boolean: Optional[bool] = ...,
    ordering: Optional[Union[str, Combinable, BaseExpression]] = ...,
    description: Optional[str] = ...,
    empty_value: Optional[str] = ...,
) -> Callable: ...
def register(*models: Type[Model], site: Optional[AdminSite] = ...) -> Callable: ...
