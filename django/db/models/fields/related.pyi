from django.core.checks.messages import (
    Error,
    Warning,
)
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.expressions import Col
from django.db.models.fields import Field
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
    ManyToOneRel,
)
from django.db.models.query_utils import (
    FilteredRelation,
    PathInfo,
)
from django.forms.models import ModelChoiceField
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from uuid import UUID


class ForeignKey:
    def __init__(
        self,
        to: Any,
        on_delete: Callable,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Any = ...,
        parent_link: bool = ...,
        to_field: Optional[str] = ...,
        db_constraint: bool = ...,
        **kwargs
    ) -> None: ...
    def _check_on_delete(self) -> List[Any]: ...
    def _check_unique(self, **kwargs) -> List[Warning]: ...
    def check(
        self,
        **kwargs
    ) -> Union[List[Error], List[Warning]]: ...
    def contribute_to_related_class(
        self,
        cls: Any,
        related: ManyToOneRel
    ) -> None: ...
    def db_check(self, connection: DatabaseWrapper) -> List[Any]: ...
    def db_parameters(self, connection: DatabaseWrapper) -> Dict[str, str]: ...
    def db_type(self, connection: DatabaseWrapper) -> str: ...
    def deconstruct(self) -> Any: ...
    def formfield(self, *, using = ..., **kwargs) -> ModelChoiceField: ...
    def get_attname(self) -> str: ...
    def get_attname_column(self) -> Tuple[str, str]: ...
    def get_col(self, alias: str, output_field: Any = ...) -> Col: ...
    def get_db_converters(self, connection: DatabaseWrapper) -> List[Any]: ...
    def get_db_prep_save(
        self,
        value: Any,
        connection: DatabaseWrapper
    ) -> Optional[Union[str, int]]: ...
    def get_db_prep_value(
        self,
        value: Union[str, UUID, int],
        connection: DatabaseWrapper,
        prepared: bool = ...
    ) -> Union[str, int]: ...
    def get_default(self) -> Optional[int]: ...
    def get_reverse_path_info(
        self,
        filtered_relation: Optional[FilteredRelation] = ...
    ) -> List[PathInfo]: ...
    @property
    def target_field(self) -> Field: ...
    def to_python(self, value: Union[str, int]) -> Union[str, int]: ...
    def validate(self, value: int, model_instance: Any) -> None: ...


class ForeignObject:
    def __init__(
        self,
        to: Any,
        on_delete: Callable,
        from_fields: Union[Tuple[str, str], List[str]],
        to_fields: Union[List[str], List[None], Tuple[str, str]],
        rel: Optional[ForeignObjectRel] = ...,
        related_name: Optional[str] = ...,
        related_query_name: None = ...,
        limit_choices_to: None = ...,
        parent_link: bool = ...,
        swappable: bool = ...,
        **kwargs
    ) -> None: ...
    def _check_to_fields_exist(self) -> List[Error]: ...
    def _check_unique_target(self) -> List[Error]: ...
    def check(self, **kwargs) -> List[Error]: ...