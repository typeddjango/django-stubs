from datetime import datetime
from django.contrib.admin.options import (
    ModelAdmin,
    TabularInline,
)
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models.base import Model
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.options import Options
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
from uuid import UUID


def _get_non_gfk_field(opts: Options, name: Union[str, Callable]) -> Any: ...


def construct_change_message(
    form: AdminPasswordChangeForm,
    formsets: None,
    add: bool
) -> List[Dict[str, Dict[str, List[str]]]]: ...


def display_for_field(value: Any, field: Any, empty_value_display: str) -> str: ...


def display_for_value(value: Any, empty_value_display: str, boolean: bool = ...) -> str: ...


def flatten(fields: Union[Tuple, List[Union[str, Callable]], List[str]]) -> Union[List[Union[str, Callable]], List[str]]: ...


def flatten_fieldsets(fieldsets: Any) -> Union[List[Union[str, Callable]], List[str]]: ...


def get_fields_from_path(model: Any, path: str) -> Any: ...


def get_model_from_relation(field: Any) -> Any: ...


def help_text_for_field(name: str, model: Any) -> str: ...


def label_for_field(
    name: Union[str, Callable],
    model: Any,
    model_admin: Optional[Union[ModelAdmin, TabularInline]] = ...,
    return_attr: bool = ...
) -> Any: ...


def lookup_field(
    name: Union[str, Callable],
    obj: Model,
    model_admin: Union[ModelAdmin, TabularInline] = ...
) -> Any: ...


def lookup_needs_distinct(opts: Options, lookup_path: str) -> bool: ...


def model_ngettext(obj: QuerySet, n: None = ...) -> str: ...


def prepare_lookup_value(key: str, value: Union[str, datetime]) -> Union[bool, datetime, str]: ...


def quote(s: Union[str, UUID, int]) -> Union[str, UUID, int]: ...


def reverse_field_path(model: Type[Model], path: str) -> Any: ...


def unquote(s: str) -> str: ...


class NestedObjects:
    def __init__(self, *args, **kwargs) -> None: ...
    def _nested(self, obj: Model, seen: Any, format_callback: Callable) -> Any: ...
    def add_edge(self, source: Any, target: Model) -> None: ...
    def can_fast_delete(self, *args, **kwargs) -> bool: ...
    def collect(self, objs: Any, source: Any = ..., source_attr: Optional[str] = ..., **kwargs) -> None: ...
    def nested(self, format_callback: Callable = ...) -> Any: ...
    def related_objects(
        self,
        related: ManyToOneRel,
        objs: Any
    ) -> QuerySet: ...