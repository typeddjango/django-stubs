from datetime import date, datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.deletion import Collector
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.reverse_related import ManyToOneRel, OneToOneRel
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.utils.safestring import SafeText


class FieldIsAForeignKeyColumnName(Exception): ...

def lookup_needs_distinct(opts: Options, lookup_path: str) -> bool: ...
def prepare_lookup_value(
    key: str, value: Union[str, datetime]
) -> Union[bool, datetime, str]: ...
def quote(s: Union[str, int]) -> Union[str, int]: ...
def unquote(s: str) -> str: ...
def flatten(
    fields: Union[
        List[Union[str, Callable]], Tuple[Tuple[str, str]], Tuple[str, str]
    ]
) -> List[Union[str, Callable]]: ...
def flatten_fieldsets(
    fieldsets: Union[
        List[Tuple[None, Dict[str, List[Union[str, Callable]]]]],
        Tuple[
            Union[
                Tuple[None, Dict[str, Tuple[Tuple[str, str]]]],
                Tuple[None, Dict[str, Tuple[str]]],
            ]
        ],
        Tuple[
            Tuple[str, Dict[str, Tuple[str]]], Tuple[str, Dict[str, Tuple[str]]]
        ],
    ]
) -> List[Union[str, Callable]]: ...
def get_deleted_objects(
    objs: QuerySet, request: WSGIRequest, admin_site: AdminSite
) -> Tuple[List[Any], Dict[Any, Any], Set[Any], List[Any]]: ...

class NestedObjects(Collector):
    data: collections.OrderedDict
    dependencies: Dict[Any, Any]
    fast_deletes: List[Any]
    field_updates: Dict[Any, Any]
    using: str
    edges: Any = ...
    protected: Any = ...
    model_objs: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def add_edge(self, source: Optional[Model], target: Model) -> None: ...
    def collect(
        self,
        objs: Union[QuerySet, List[Model]],
        source: Optional[Type[Model]] = ...,
        source_attr: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def related_objects(
        self, related: ManyToOneRel, objs: List[Model]
    ) -> QuerySet: ...
    def nested(
        self, format_callback: Callable = ...
    ) -> Union[
        List[Union[List[str], str]], List[Union[SafeText, List[SafeText]]]
    ]: ...
    def can_fast_delete(self, *args: Any, **kwargs: Any) -> bool: ...

def model_format_dict(obj: Any): ...
def model_ngettext(obj: QuerySet, n: None = ...) -> str: ...
def lookup_field(
    name: Union[str, Callable], obj: Model, model_admin: BaseModelAdmin = ...
) -> Union[
    Tuple[
        Union[str, Model, date, int, None],
        Union[str, Model, date, int, None],
        Union[str, Model, date, int, None],
    ],
    Tuple[None, Callable, Callable],
]: ...
def label_for_field(
    name: Union[str, Callable],
    model: Type[Model],
    model_admin: BaseModelAdmin = ...,
    return_attr: bool = ...,
) -> Union[
    Tuple[
        Union[Type[str], None, Callable, GenericForeignKey],
        Union[Type[str], None, Callable, GenericForeignKey],
    ],
    str,
]: ...
def help_text_for_field(name: str, model: Type[Model]) -> str: ...
def display_for_field(
    value: Optional[Union[int, str, date, Model]],
    field: Union[Field, reverse_related.OneToOneRel],
    empty_value_display: SafeText,
) -> str: ...
def display_for_value(
    value: Optional[Union[Callable, Model, int, str]],
    empty_value_display: SafeText,
    boolean: bool = ...,
) -> str: ...

class NotRelationField(Exception): ...

def get_model_from_relation(
    field: Union[Field, reverse_related.ManyToOneRel]
) -> Type[Model]: ...
def reverse_field_path(
    model: Type[Model], path: str
) -> Tuple[Type[Model], str]: ...
def get_fields_from_path(
    model: Type[Model], path: str
) -> List[Union[FieldCacheMixin, Field]]: ...
def construct_change_message(form: Any, formsets: Any, add: Any): ...
