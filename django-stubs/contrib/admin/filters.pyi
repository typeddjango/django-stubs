from collections.abc import Callable, Iterable, Iterator
from typing import Any

from django.contrib.admin.options import ModelAdmin
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.functional import _StrOrPromise

class ListFilter:
    title: _StrOrPromise | None
    template: str
    used_parameters: Any
    def __init__(
        self, request: HttpRequest, params: dict[str, str], model: type[Model], model_admin: ModelAdmin
    ) -> None: ...
    def has_output(self) -> bool: ...
    def choices(self, changelist: Any) -> Iterator[dict[str, Any]]: ...
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None: ...
    def expected_parameters(self) -> list[str | None]: ...

class SimpleListFilter(ListFilter):
    parameter_name: str | None
    lookup_choices: Any
    def value(self) -> str | None: ...
    def lookups(self, request: HttpRequest, model_admin: ModelAdmin) -> Iterable[tuple[Any, str]] | None: ...

class FieldListFilter(ListFilter):
    field: Field
    field_path: str
    title: _StrOrPromise
    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None: ...
    @classmethod
    def register(cls, test: Callable, list_filter_class: type[FieldListFilter], take_priority: bool = ...) -> None: ...
    @classmethod
    def create(
        cls,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> FieldListFilter: ...

class RelatedFieldListFilter(FieldListFilter):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: Any
    lookup_val_isnull: Any
    lookup_choices: Any
    lookup_title: str
    empty_value_display: Any
    @property
    def include_empty_choice(self) -> bool: ...
    def field_choices(
        self, field: RelatedField, request: HttpRequest, model_admin: ModelAdmin
    ) -> list[tuple[str, str]]: ...

class BooleanFieldListFilter(FieldListFilter):
    lookup_kwarg: str
    lookup_kwarg2: str
    lookup_val: Any
    lookup_val2: Any

class ChoicesFieldListFilter(FieldListFilter):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: Any
    lookup_val_isnull: Any

class DateFieldListFilter(FieldListFilter):
    field_generic: Any
    date_params: Any
    lookup_kwarg_since: Any
    lookup_kwarg_until: Any
    links: Any
    lookup_kwarg_isnull: Any

class AllValuesFieldListFilter(FieldListFilter):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: Any
    lookup_val_isnull: Any
    empty_value_display: str
    lookup_choices: QuerySet

class RelatedOnlyFieldListFilter(RelatedFieldListFilter): ...

class EmptyFieldListFilter(FieldListFilter):
    lookup_kwarg: str
    lookup_val: Any
