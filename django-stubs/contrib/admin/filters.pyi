from collections.abc import Callable, Iterable, Iterator
from datetime import date, datetime
from typing import Any, ClassVar, Generic, TypeVar

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models.aggregates import Count
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http.request import HttpRequest
from django.utils.datastructures import _ListOrTuple
from django.utils.functional import _StrOrPromise
from django.utils.safestring import SafeString
from typing_extensions import TypedDict

class _ListFilterChoices(TypedDict):
    selected: bool
    query_string: str
    display: _StrOrPromise

_ModelT = TypeVar("_ModelT", bound=Model)
_ST = TypeVar("_ST", contravariant=True)
_GT = TypeVar("_GT", covariant=True)

class ListFilter(Generic[_ModelT]):
    title: _StrOrPromise | None
    template: str
    request: HttpRequest
    used_parameters: dict[str, bool | datetime | str]
    def __init__(
        self, request: HttpRequest, params: dict[str, str], model: type[Model], model_admin: ModelAdmin[_ModelT]
    ) -> None: ...
    def has_output(self) -> bool: ...
    def choices(self, changelist: ChangeList) -> Iterator[_ListFilterChoices]: ...
    def queryset(self, request: HttpRequest, queryset: QuerySet[_ModelT]) -> QuerySet[_ModelT] | None: ...
    def expected_parameters(self) -> list[str | None]: ...

class FacetsMixin:
    def get_facet_counts(self, pk_attname: str, filtered_qs: QuerySet[Model]) -> dict[str, Count]: ...
    def get_facet_queryset(self, changelist: ChangeList) -> dict[str, int]: ...

class SimpleListFilter(FacetsMixin, ListFilter[_ModelT]):
    parameter_name: str | None
    lookup_choices: list[tuple[str, _StrOrPromise]]
    def value(self) -> str | None: ...
    def lookups(
        self, request: HttpRequest, model_admin: ModelAdmin[_ModelT]
    ) -> Iterable[tuple[str, _StrOrPromise]] | None: ...

class FieldListFilter(FacetsMixin, ListFilter[_ModelT], Generic[_ModelT, _ST, _GT]):
    list_separator: ClassVar[str]
    field: Field[_ST, _GT]
    field_path: str
    title: _StrOrPromise
    def __init__(
        self,
        field: Field[_ST, _GT],
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin[_ModelT],
        field_path: str,
    ) -> None: ...
    @classmethod
    def register(
        cls,
        test: Callable[[Field[_ST, _GT]], Any],
        list_filter_class: type[FieldListFilter[_ModelT, _ST, _GT]],
        take_priority: bool = ...,
    ) -> None: ...
    @classmethod
    def create(
        cls,
        field: Field[_ST, _GT],
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin[_ModelT],
        field_path: str,
    ) -> FieldListFilter[_ModelT, _ST, _GT]: ...

class RelatedFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: str | None
    lookup_val_isnull: str | None
    lookup_choices: list[tuple[str, _StrOrPromise]]
    lookup_title: _StrOrPromise
    empty_value_display: SafeString
    @property
    def include_empty_choice(self) -> bool: ...
    def field_admin_ordering(
        self, field: RelatedField[_ST, _GT], request: HttpRequest, model_admin: ModelAdmin[_ModelT]
    ) -> _ListOrTuple[str]: ...
    def field_choices(
        self, field: RelatedField[_ST, _GT], request: HttpRequest, model_admin: ModelAdmin[_ModelT]
    ) -> list[tuple[str, _StrOrPromise]]: ...

class BooleanFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    lookup_kwarg: str
    lookup_kwarg2: str
    lookup_val: str | None
    lookup_val2: str | None

class ChoicesFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: str | None
    lookup_val_isnull: str | None

class DateFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    field_generic: str
    date_params: dict[str, str]
    lookup_kwarg_since: str
    lookup_kwarg_until: str
    links: tuple[tuple[_StrOrPromise, dict[str, bool | date | datetime]], ...]
    lookup_kwarg_isnull: str

class AllValuesFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    lookup_kwarg: str
    lookup_kwarg_isnull: str
    lookup_val: str | None
    lookup_val_isnull: str | None
    empty_value_display: SafeString
    lookup_choices: QuerySet[_ModelT]

class RelatedOnlyFieldListFilter(RelatedFieldListFilter[_ModelT, _ST, _GT]): ...

class EmptyFieldListFilter(FieldListFilter[_ModelT, _ST, _GT]):
    lookup_kwarg: str
    lookup_val: str | None
    def get_lookup_condition(self) -> Q: ...
