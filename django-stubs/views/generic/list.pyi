from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import (
    Page,
    Paginator,
)
from django.db.models.query import QuerySet
from django.template.response import TemplateResponse
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class BaseListView:
    def get(
        self,
        request: WSGIRequest,
        *args,
        **kwargs
    ) -> TemplateResponse: ...


class MultipleObjectMixin:
    def get_allow_empty(self) -> bool: ...
    def get_context_data(self, *, object_list = ..., **kwargs) -> Dict[str, Any]: ...
    def get_context_object_name(
        self,
        object_list: Optional[Union[List[Dict[str, str]], QuerySet]]
    ) -> Optional[str]: ...
    def get_ordering(self) -> None: ...
    def get_paginate_by(self, queryset: Union[List[Dict[str, str]], QuerySet]) -> Optional[int]: ...
    def get_paginate_orphans(self) -> int: ...
    def get_paginator(
        self,
        queryset: QuerySet,
        per_page: int,
        orphans: int = ...,
        allow_empty_first_page: bool = ...,
        **kwargs
    ) -> Paginator: ...
    def get_queryset(self) -> Union[List[Dict[str, str]], QuerySet]: ...
    def paginate_queryset(
        self,
        queryset: QuerySet,
        page_size: int
    ) -> Tuple[Paginator, Page, QuerySet, bool]: ...


class MultipleObjectTemplateResponseMixin:
    def get_template_names(self) -> List[str]: ...