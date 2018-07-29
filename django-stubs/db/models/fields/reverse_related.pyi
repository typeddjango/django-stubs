from django.db.models.base import Model
from django.db.models.fields import (
    AutoField,
    Field,
)
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    RelatedField,
)
from django.db.models.fields.related_lookups import (
    RelatedExact,
    RelatedIn,
    RelatedIsNull,
)
from django.db.models.query_utils import (
    FilteredRelation,
    PathInfo,
)
from django.db.models.sql.where import WhereNode
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


class ForeignObjectRel:
    def __init__(
        self,
        field: RelatedField,
        to: Any,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Any = ...,
        parent_link: bool = ...,
        on_delete: Optional[Callable] = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def db_type(self) -> Callable: ...
    def get_accessor_name(self, model: Optional[Type[Model]] = ...) -> Optional[str]: ...
    def get_cache_name(self) -> str: ...
    def get_choices(
        self,
        include_blank: bool = ...,
        blank_choice: List[Tuple[str, str]] = ...
    ) -> List[Tuple[int, str]]: ...
    def get_extra_restriction(
        self,
        where_class: Type[WhereNode],
        alias: str,
        related_alias: str
    ) -> Optional[WhereNode]: ...
    def get_internal_type(self) -> str: ...
    def get_joining_columns(self) -> Union[Tuple[Tuple[str, str]], Tuple[Tuple[str, str], Tuple[str, str]]]: ...
    def get_lookup(
        self,
        lookup_name: str
    ) -> Type[Union[RelatedIsNull, RelatedExact, RelatedIn]]: ...
    def get_path_info(
        self,
        filtered_relation: Optional[FilteredRelation] = ...
    ) -> List[PathInfo]: ...
    @cached_property
    def hidden(self) -> bool: ...
    def is_hidden(self) -> bool: ...
    @cached_property
    def many_to_many(self) -> bool: ...
    @cached_property
    def many_to_one(self) -> bool: ...
    @cached_property
    def name(self) -> str: ...
    @cached_property
    def one_to_many(self) -> bool: ...
    @cached_property
    def one_to_one(self) -> bool: ...
    @cached_property
    def related_model(self) -> Type[Model]: ...
    @property
    def remote_field(
        self
    ) -> Union[ManyToManyField, ForeignKey]: ...
    def set_field_name(self) -> None: ...
    @property
    def target_field(self) -> AutoField: ...


class ManyToManyRel:
    def __init__(
        self,
        field: RelatedField,
        to: Any,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[Callable] = ...,
        symmetrical: bool = ...,
        through: Optional[Union[str, Type[Model]]] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...
    ) -> None: ...
    def get_related_field(self) -> Field: ...


class ManyToOneRel:
    def __getstate__(self) -> Dict[str, Any]: ...
    def __init__(
        self,
        field: ForeignKey,
        to: Any,
        field_name: Optional[str],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Any = ...,
        parent_link: bool = ...,
        on_delete: Callable = ...
    ) -> None: ...