from datetime import date, datetime
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union
from uuid import UUID

from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.deletion import Collector
from django.db.models.fields import Field
from django.db.models.fields.files import FieldFile
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.reverse_related import (ForeignObjectRel,
                                                     ManyToOneRel)
from django.db.models.options import Options
from django.db.models.query import QuerySet


class FieldIsAForeignKeyColumnName(Exception): ...

def lookup_needs_distinct(opts: Options, lookup_path: str) -> bool: ...
def prepare_lookup_value(
    key: str, value: Union[datetime, str]
) -> Union[bool, datetime, str]: ...
def quote(s: Union[int, str, UUID]) -> Union[int, str, UUID]: ...
def unquote(s: str) -> str: ...
def flatten(
    fields: Union[
        List[Union[Callable, str]],
        List[Union[List[str], str]],
        List[Union[Tuple[str, str], str]],
        Tuple,
    ]
) -> List[Union[Callable, str]]: ...
def flatten_fieldsets(
    fieldsets: Union[
        List[
            Tuple[
                None,
                Union[
                    Dict[str, List[Any]],
                    Dict[str, List[Union[Callable, str]]],
                    Dict[str, List[str]],
                    Dict[str, Tuple[str, str]],
                ],
            ]
        ],
        List[Tuple[str, Dict[str, Union[Tuple[str, str], Tuple[str]]]]],
        Tuple[
            Tuple[
                None,
                Union[
                    Dict[str, Tuple[Tuple[str, str]]],
                    Dict[str, Tuple[str, str, List[str]]],
                    Dict[str, Tuple[str, str, Tuple[str, str]]],
                    Dict[str, Union[Tuple[str, str, str], Tuple[str]]],
                ],
            ]
        ],
        Tuple[
            Tuple[str, Dict[str, Union[Tuple[str, str], Tuple[str]]]],
            Tuple[
                str,
                Union[
                    Dict[str, Union[Tuple[str, str, str], Tuple[str]]],
                    Dict[str, Union[Tuple[str, str], Tuple[str]]],
                ],
            ],
        ],
    ]
) -> List[Union[Callable, str]]: ...
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
        objs: Union[List[Model], QuerySet],
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
        List[Union[List[Union[List[int], int]], int]],
        List[Union[List[Union[List[str], str]], str]],
    ]: ...
    def can_fast_delete(self, *args: Any, **kwargs: Any) -> bool: ...

def model_format_dict(obj: Any): ...
def model_ngettext(
    obj: Union[Options, QuerySet], n: Optional[int] = ...
) -> str: ...
def lookup_field(
    name: Union[Callable, str], obj: Model, model_admin: BaseModelAdmin = ...
) -> Union[
    Tuple[None, Callable, Optional[Union[Callable, date, int, str]]],
    Tuple[
        Optional[Union[date, Model, FieldFile, float, int, str]],
        Optional[Union[date, Model, FieldFile, float, int, str]],
        Optional[Union[date, Model, FieldFile, float, int, str]],
    ],
]: ...
def label_for_field(
    name: Union[Callable, str],
    model: Type[Model],
    model_admin: Optional[BaseModelAdmin] = ...,
    return_attr: bool = ...,
) -> Union[
    Tuple[Callable, Callable],
    Tuple[str, Optional[Union[Type[str], GenericForeignKey]]],
    str,
]: ...
def help_text_for_field(name: str, model: Type[Model]) -> str: ...
def display_for_field(
    value: Optional[Union[date, Decimal, Model, FieldFile, float, int, str]],
    field: Union[Field, mixins.FieldCacheMixin],
    empty_value_display: str,
) -> str: ...
def display_for_value(
    value: Optional[
        Union[Callable, List[Union[int, str]], date, Model, FieldFile, int, str]
    ],
    empty_value_display: str,
    boolean: bool = ...,
) -> str: ...

class NotRelationField(Exception): ...

def get_model_from_relation(
    field: Union[Field, ForeignObjectRel]
) -> Type[Model]: ...
def reverse_field_path(
    model: Type[Model], path: str
) -> Tuple[Type[Model], str]: ...
def get_fields_from_path(
    model: Type[Model], path: str
) -> List[Union[Field, ForeignObjectRel]]: ...
def construct_change_message(
    form: AdminPasswordChangeForm, formsets: None, add: bool
) -> List[Dict[str, Dict[str, List[str]]]]: ...
