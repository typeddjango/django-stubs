import sys
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Type, TypeVar, Union, overload
from uuid import UUID

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from django.core import validators  # due to weird mypy.stubtest error
from django.db import models
from django.db.models.base import Model
from django.db.models.expressions import Combinable
from django.db.models.fields import Field, _AllLimitChoicesTo, _ErrorMessagesT, _FieldChoices, _LimitChoicesTo
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor as ForwardManyToOneDescriptor
from django.db.models.fields.related_descriptors import (  # noqa: F401
    ForwardOneToOneDescriptor as ForwardOneToOneDescriptor,
)
from django.db.models.fields.related_descriptors import ManyToManyDescriptor as ManyToManyDescriptor
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor as ReverseManyToOneDescriptor
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor as ReverseOneToOneDescriptor
from django.db.models.fields.reverse_related import ForeignObjectRel as ForeignObjectRel  # noqa: F401
from django.db.models.fields.reverse_related import ManyToManyRel as ManyToManyRel
from django.db.models.fields.reverse_related import ManyToOneRel as ManyToOneRel
from django.db.models.fields.reverse_related import OneToOneRel as OneToOneRel
from django.db.models.manager import RelatedManager
from django.db.models.query_utils import FilteredRelation, PathInfo, Q

_T = TypeVar("_T", bound=models.Model)
_F = TypeVar("_F", bound=models.Field)

RECURSIVE_RELATIONSHIP_CONSTANT: Literal["self"] = ...

def resolve_relation(scope_model: Type[Model], relation: Union[str, Type[Model]]) -> Union[str, Type[Model]]: ...

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class RelatedField(FieldCacheMixin, Field[_ST, _GT]):
    one_to_many: bool = ...
    one_to_one: bool = ...
    many_to_many: bool = ...
    many_to_one: bool = ...
    opts: Any = ...

    remote_field: ForeignObjectRel
    rel_class: Type[ForeignObjectRel]
    swappable: bool
    @property
    def related_model(self) -> Type[Model]: ...  # type: ignore
    def get_forward_related_filter(self, obj: Model) -> Dict[str, Union[int, UUID]]: ...
    def get_reverse_related_filter(self, obj: Model) -> Q: ...
    @property
    def swappable_setting(self) -> Optional[str]: ...
    def set_attributes_from_rel(self) -> None: ...
    def do_related_class(self, other: Type[Model], cls: Type[Model]) -> None: ...
    def get_limit_choices_to(self) -> _LimitChoicesTo: ...
    def related_query_name(self) -> str: ...
    @property
    def target_field(self) -> Field: ...

class ForeignObject(RelatedField[_ST, _GT]):
    remote_field: ForeignObjectRel
    rel_class: Type[ForeignObjectRel]
    swappable: bool
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Callable[..., None],
        from_fields: Sequence[str],
        to_fields: Sequence[str],
        rel: Optional[ForeignObjectRel] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_AllLimitChoicesTo] = ...,
        parent_link: bool = ...,
        swappable: bool = ...,
        *,
        db_constraint: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...
    def resolve_related_fields(self) -> List[Tuple[Field, Field]]: ...
    @property
    def related_fields(self) -> List[Tuple[Field, Field]]: ...
    @property
    def reverse_related_fields(self) -> List[Tuple[Field, Field]]: ...
    @property
    def local_related_fields(self) -> Tuple[Field, ...]: ...
    @property
    def foreign_related_fields(self) -> Tuple[Field, ...]: ...

class ForeignKey(ForeignObject[_ST, _GT]):
    _pyi_private_set_type: Union[Any, Combinable]
    _pyi_private_get_type: Any

    remote_field: ManyToOneRel
    rel_class: Type[ManyToOneRel]
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Callable[..., None],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_AllLimitChoicesTo] = ...,
        parent_link: bool = ...,
        to_field: Optional[str] = ...,
        db_constraint: bool = ...,
        *,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner) -> ForwardManyToOneDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> _GT: ...
    # non-Model instances
    @overload
    def __get__(self: _F, instance, owner) -> _F: ...

class OneToOneField(ForeignKey[_ST, _GT]):
    _pyi_private_set_type: Union[Any, Combinable]
    _pyi_private_get_type: Any

    remote_field: OneToOneRel
    rel_class: Type[OneToOneRel]
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Any,
        to_field: Optional[str] = ...,
        *,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_AllLimitChoicesTo] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner) -> ForwardOneToOneDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> _GT: ...
    # non-Model instances
    @overload
    def __get__(self: _F, instance, owner) -> _F: ...

class ManyToManyField(RelatedField[_ST, _GT]):
    _pyi_private_set_type: Sequence[Any]
    _pyi_private_get_type: RelatedManager[Any]

    description: str = ...
    has_null_arg: bool = ...
    swappable: bool = ...

    many_to_many: Literal[True]
    many_to_one: Literal[False]
    one_to_many: Literal[False]
    one_to_one: Literal[False]

    remote_field: ManyToManyRel
    rel_class: Type[ManyToManyRel]
    def __init__(
        self,
        to: Union[Type[Model], str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_AllLimitChoicesTo] = ...,
        symmetrical: Optional[bool] = ...,
        through: Union[str, Type[Model], None] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...,
        db_table: Optional[str] = ...,
        swappable: bool = ...,
        *,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ) -> None: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner) -> ManyToManyDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> _GT: ...
    # non-Model instances
    @overload
    def __get__(self: _F, instance, owner) -> _F: ...
    def get_path_info(self, filtered_relation: Optional[FilteredRelation] = ...) -> List[PathInfo]: ...
    def get_reverse_path_info(self, filtered_relation: Optional[FilteredRelation] = ...) -> List[PathInfo]: ...
    def contribute_to_related_class(self, cls: Type[Model], related: RelatedField) -> None: ...
    def m2m_db_table(self) -> str: ...
    def m2m_column_name(self) -> str: ...
    def m2m_reverse_name(self) -> str: ...
    def m2m_reverse_field_name(self) -> str: ...
    def m2m_target_field_name(self) -> str: ...
    def m2m_reverse_target_field_name(self) -> str: ...

def create_many_to_many_intermediary_model(field: ManyToManyField, klass: Type[Model]) -> Type[Model]: ...
