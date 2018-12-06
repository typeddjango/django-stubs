from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.db.models.base import Model
from django.db.models.fields import AutoField, Field
from django.db.models.fields.related import ForeignKey, OneToOneField, RelatedField
from django.db.models.lookups import BuiltinLookup, StartsWith
from django.db.models.query_utils import FilteredRelation, PathInfo, Q
from django.db.models.sql.where import WhereNode

from .mixins import FieldCacheMixin

class ForeignObjectRel(FieldCacheMixin):
    hidden: bool
    many_to_many: bool
    many_to_one: bool
    name: str
    one_to_many: bool
    one_to_one: bool
    related_model: Type[django.db.models.base.Model]
    auto_created: bool = ...
    concrete: bool = ...
    editable: bool = ...
    is_relation: bool = ...
    null: bool = ...
    field: django.db.models.fields.related.ForeignObject = ...
    model: Union[Type[django.db.models.base.Model], str] = ...
    related_name: Optional[str] = ...
    related_query_name: None = ...
    limit_choices_to: Dict[Any, Any] = ...
    parent_link: bool = ...
    on_delete: Callable = ...
    symmetrical: bool = ...
    multiple: bool = ...
    def __init__(
        self,
        field: RelatedField,
        to: Union[Type[Model], str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Callable, Dict[str, Union[int, str]], Q]] = ...,
        parent_link: bool = ...,
        on_delete: Optional[Callable] = ...,
    ) -> None: ...
    def hidden(self) -> bool: ...
    def name(self) -> str: ...
    @property
    def remote_field(self) -> RelatedField: ...
    @property
    def target_field(self) -> AutoField: ...
    def related_model(self) -> Type[Model]: ...
    def many_to_many(self) -> bool: ...
    def many_to_one(self) -> bool: ...
    def one_to_many(self) -> bool: ...
    def one_to_one(self) -> bool: ...
    def get_lookup(self, lookup_name: str) -> Type[BuiltinLookup]: ...
    def get_internal_type(self) -> str: ...
    @property
    def db_type(self) -> Callable: ...
    def get_choices(
        self, include_blank: bool = ..., blank_choice: List[Tuple[str, str]] = ...
    ) -> List[Tuple[int, str]]: ...
    def is_hidden(self) -> bool: ...
    def get_joining_columns(self) -> Tuple: ...
    def get_extra_restriction(
        self, where_class: Type[WhereNode], alias: str, related_alias: str
    ) -> Optional[Union[StartsWith, WhereNode]]: ...
    field_name: None = ...
    def set_field_name(self) -> None: ...
    def get_accessor_name(self, model: Optional[Type[Model]] = ...) -> Optional[str]: ...
    def get_path_info(self, filtered_relation: Optional[FilteredRelation] = ...) -> List[PathInfo]: ...
    def get_cache_name(self) -> str: ...

class ManyToOneRel(ForeignObjectRel):
    field: django.db.models.fields.related.ForeignKey
    hidden: bool
    limit_choices_to: Union[Callable, Dict[str, Union[int, str]], django.db.models.query_utils.Q]
    many_to_many: bool
    many_to_one: bool
    model: Union[Type[django.db.models.base.Model], str]
    multiple: bool
    name: str
    on_delete: Callable
    one_to_many: bool
    one_to_one: bool
    parent_link: bool
    related_model: Type[django.db.models.base.Model]
    related_name: Optional[str]
    related_query_name: Optional[str]
    symmetrical: bool
    field_name: Optional[str] = ...
    def __init__(
        self,
        field: ForeignKey,
        to: Union[Type[Model], str],
        field_name: Optional[str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Callable, Dict[str, Union[int, str]], Q]] = ...,
        parent_link: bool = ...,
        on_delete: Callable = ...,
    ) -> None: ...
    def get_related_field(self) -> Field: ...
    def set_field_name(self) -> None: ...

class OneToOneRel(ManyToOneRel):
    field: django.db.models.fields.related.OneToOneField
    field_name: Optional[str]
    hidden: bool
    limit_choices_to: Dict[str, str]
    many_to_many: bool
    many_to_one: bool
    model: Union[Type[django.db.models.base.Model], str]
    name: str
    on_delete: Callable
    one_to_many: bool
    one_to_one: bool
    parent_link: bool
    related_model: Type[django.db.models.base.Model]
    related_name: Optional[str]
    related_query_name: Optional[str]
    symmetrical: bool
    multiple: bool = ...
    def __init__(
        self,
        field: OneToOneField,
        to: Union[Type[Model], str],
        field_name: Optional[str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Dict[str, str]] = ...,
        parent_link: bool = ...,
        on_delete: Callable = ...,
    ) -> None: ...

class ManyToManyRel(ForeignObjectRel):
    field: django.db.models.fields.related.RelatedField
    field_name: None
    hidden: bool
    limit_choices_to: Union[Callable, Dict[str, str]]
    model: Union[Type[django.db.models.base.Model], str]
    multiple: bool
    name: str
    on_delete: None
    one_to_many: bool
    one_to_one: bool
    parent_link: bool
    related_model: Type[django.db.models.base.Model]
    related_name: Optional[str]
    related_query_name: Optional[str]
    through: Optional[Union[Type[django.db.models.base.Model], str]] = ...
    through_fields: Optional[Tuple[str, str]] = ...
    symmetrical: bool = ...
    db_constraint: bool = ...
    def __init__(
        self,
        field: RelatedField,
        to: Union[Type[Model], str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Callable, Dict[str, str]]] = ...,
        symmetrical: bool = ...,
        through: Optional[Union[Type[Model], str]] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...,
    ) -> None: ...
    def get_related_field(self) -> Field: ...
