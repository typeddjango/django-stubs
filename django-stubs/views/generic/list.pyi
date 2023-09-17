from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from django.core.paginator import Page, Paginator, _SupportsPagination
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View

_M = TypeVar("_M", bound=Model, covariant=True)

class MultipleObjectMixin(Generic[_M], ContextMixin):
    allow_empty: bool
    queryset: _SupportsPagination[_M] | None
    model: type[_M] | None
    paginate_by: int | None
    paginate_orphans: int
    context_object_name: str | None
    paginator_class: type[Paginator]
    page_kwarg: str
    ordering: str | Sequence[str] | None
    def get_queryset(self) -> _SupportsPagination[_M]: ...
    def get_ordering(self) -> str | Sequence[str] | None: ...
    def paginate_queryset(
        self, queryset: _SupportsPagination[_M], page_size: int
    ) -> tuple[Paginator, Page, _SupportsPagination[_M], bool]: ...
    def get_paginate_by(self, queryset: _SupportsPagination[_M]) -> int | None: ...
    def get_paginator(
        self,
        queryset: _SupportsPagination[_M],
        per_page: int,
        orphans: int = ...,
        allow_empty_first_page: bool = ...,
        **kwargs: Any,
    ) -> Paginator: ...
    def get_paginate_orphans(self) -> int: ...
    def get_allow_empty(self) -> bool: ...
    def get_context_object_name(self, object_list: _SupportsPagination[_M]) -> str | None: ...
    def get_context_data(
        self, *, object_list: _SupportsPagination[_M] | None = ..., **kwargs: Any
    ) -> dict[str, Any]: ...

class BaseListView(MultipleObjectMixin[_M], View):
    object_list: _SupportsPagination[_M]
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...

class MultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    template_name_suffix: str

class ListView(MultipleObjectTemplateResponseMixin, BaseListView[_M]): ...
