from collections import OrderedDict
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.expressions import CombinedExpression
from django.db.models.query import QuerySet
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


class ChangeList:
    def __init__(
        self,
        request: WSGIRequest,
        model: Type[Model],
        list_display: Union[List[str], List[Union[str, Callable]], Tuple[str, str, str, str]],
        list_display_links: Union[List[str], Tuple[str, str]],
        list_filter: Union[List[Type[SimpleListFilter]], List[str], Tuple],
        date_hierarchy: Optional[str],
        search_fields: Union[List[str], Tuple],
        list_select_related: bool,
        list_per_page: int,
        list_max_show_all: int,
        list_editable: Union[List[str], Tuple],
        model_admin: ModelAdmin,
        sortable_by: Any
    ) -> None: ...
    def _get_default_ordering(self) -> Union[List[str], Tuple[str], Tuple[str, str]]: ...
    def apply_select_related(self, qs: QuerySet) -> QuerySet: ...
    def get_filters(self, request: WSGIRequest) -> Any: ...
    def get_filters_params(self, params: None = ...) -> Dict[str, str]: ...
    def get_ordering(
        self,
        request: WSGIRequest,
        queryset: QuerySet
    ) -> List[str]: ...
    def get_ordering_field(
        self,
        field_name: Union[str, Callable]
    ) -> Optional[Union[str, CombinedExpression]]: ...
    def get_ordering_field_columns(self) -> OrderedDict: ...
    def get_query_string(self, new_params: Any = ..., remove: Optional[List[str]] = ...) -> str: ...
    def get_queryset(self, request: WSGIRequest) -> QuerySet: ...
    def get_results(self, request: WSGIRequest) -> None: ...
    def has_related_field_in_list_display(self) -> bool: ...
    def url_for_result(self, result: Model) -> str: ...