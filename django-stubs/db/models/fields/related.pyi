from typing import (
    Type,
    Union,
    TypeVar,
    Any,
    Generic,
    List,
    Optional,
    Dict,
    Callable,
    Tuple,
    Sequence,
    TYPE_CHECKING,
    Iterable,
)
from uuid import UUID

from django.db import models
from django.db.models import Field, Model, QuerySet
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related_descriptors import (
    ReverseManyToOneDescriptor as ReverseManyToOneDescriptor,
    ReverseOneToOneDescriptor as ReverseOneToOneDescriptor,
    ForwardManyToOneDescriptor as ForwardManyToOneDescriptor,
    ForwardOneToOneDescriptor as ForwardOneToOneDescriptor,
    ManyToManyDescriptor as ManyToManyDescriptor,
)
from django.db.models.fields.reverse_related import (
    ForeignObjectRel as ForeignObjectRel,
    ManyToManyRel as ManyToManyRel,
    ManyToOneRel as ManyToOneRel,
    OneToOneRel as OneToOneRel,
)
from django.db.models.query_utils import PathInfo, Q

from django.db.models.expressions import Combinable

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

_T = TypeVar("_T", bound=models.Model)

_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]

_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

RECURSIVE_RELATIONSHIP_CONSTANT: str = ...

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class RelatedField(FieldCacheMixin, Field[_ST, _GT]):
    one_to_many: bool = ...
    one_to_one: bool = ...
    many_to_many: bool = ...
    many_to_one: bool = ...
    def related_model(self) -> Union[Type[Model], str]: ...
    def check(self, **kwargs: Any) -> List[Any]: ...
    opts: Any = ...
    def deconstruct(self) -> Tuple[Optional[str], str, List[Any], Dict[str, str]]: ...
    def get_forward_related_filter(self, obj: Model) -> Dict[str, Union[int, UUID]]: ...
    def get_reverse_related_filter(self, obj: Model) -> Q: ...
    @property
    def swappable_setting(self) -> Optional[str]: ...
    name: Any = ...
    verbose_name: Any = ...
    def set_attributes_from_rel(self) -> None: ...
    def do_related_class(self, other: Type[Model], cls: Type[Model]) -> None: ...
    def get_limit_choices_to(self) -> Dict[str, int]: ...
    def related_query_name(self) -> str: ...
    @property
    def target_field(self) -> Field: ...

class ForeignObject(RelatedField):
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Callable[..., None],
        from_fields: Sequence[str],
        to_fields: Sequence[str],
        rel: None = ...,
        related_name: Optional[str] = ...,
        related_query_name: None = ...,
        limit_choices_to: Optional[Union[Dict[str, Any], Callable[[], Any]]] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...

class ForeignKey(RelatedField[_ST, _GT]):
    _pyi_private_set_type: Union[Any, Combinable]
    _pyi_private_get_type: Any
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Callable[..., None],
        to_field: Optional[str] = ...,
        related_name: str = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Dict[str, Any], Callable[[], Any], Q]] = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...

class OneToOneField(RelatedField[_ST, _GT]):
    _pyi_private_set_type: Union[Any, Combinable]
    _pyi_private_get_type: Any
    def __init__(
        self,
        to: Union[Type[Model], str],
        on_delete: Any,
        to_field: Optional[str] = ...,
        related_name: str = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Dict[str, Any], Callable[[], Any], Q]] = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...

class ManyToManyField(RelatedField[_ST, _GT]):
    _pyi_private_set_type: Sequence[Any]
    _pyi_private_get_type: RelatedManager[Any]

    many_to_many: bool = ...
    many_to_one: bool = ...
    one_to_many: bool = ...
    one_to_one: bool = ...
    rel_class: Any = ...
    description: Any = ...
    has_null_arg: Any = ...
    swappable: Any = ...
    def __init__(
        self,
        to: Union[Type[_T], str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Union[Dict[str, Any], Callable[[], Any], Q]] = ...,
        symmetrical: Optional[bool] = ...,
        through: Optional[Union[str, Type[Model]]] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...,
        db_table: Optional[str] = ...,
        swappable: bool = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    def check(self, **kwargs: Any) -> List[Any]: ...
    def deconstruct(self) -> Tuple[Optional[str], str, List[Any], Dict[str, str]]: ...
    def get_path_info(self, filtered_relation: None = ...) -> List[PathInfo]: ...
    def get_reverse_path_info(self, filtered_relation: None = ...) -> List[PathInfo]: ...
    m2m_db_table: Any = ...
    m2m_column_name: Any = ...
    m2m_reverse_name: Any = ...
    m2m_field_name: Any = ...
    m2m_reverse_field_name: Any = ...
    m2m_target_field_name: Any = ...
    m2m_reverse_target_field_name: Any = ...
    def contribute_to_related_class(self, cls: Type[Model], related: RelatedField) -> None: ...
    def set_attributes_from_rel(self) -> None: ...
    def value_from_object(self, obj: Model) -> List[Model]: ...
    def save_form_data(self, instance: Model, data: QuerySet) -> None: ...

def create_many_to_many_intermediary_model(field: Type[Field], klass: Type[Model]) -> Type[Model]: ...
