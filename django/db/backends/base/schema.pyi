from django.db.backends.ddl_references import Statement
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.models.base import Model
from django.db.models.fields import Field
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


class BaseDatabaseSchemaEditor:
    def __enter__(self) -> DatabaseSchemaEditor: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...
    def __init__(
        self,
        connection: DatabaseWrapper,
        collect_sql: bool = ...,
        atomic: bool = ...
    ) -> None: ...
    def _constraint_names(
        self,
        model: Type[Model],
        column_names: List[str] = ...,
        unique: Optional[bool] = ...,
        primary_key: None = ...,
        index: Optional[bool] = ...,
        foreign_key: None = ...,
        check: None = ...,
        type_: None = ...
    ) -> List[str]: ...
    def _create_index_name(
        self,
        table_name: str,
        column_names: Union[Tuple[str, str, str], Tuple[str], List[str]],
        suffix: str = ...
    ) -> str: ...
    def _create_index_sql(
        self,
        model: Any,
        fields: Any,
        *,
        name = ...,
        suffix = ...,
        using = ...,
        db_tablespace = ...,
        col_suffixes = ...,
        sql = ...
    ) -> Statement: ...
    def _create_unique_sql(self, model: Any, columns: List[str]) -> Statement: ...
    def _delete_composed_index(
        self,
        model: Type[Model],
        fields: Tuple[str, str],
        constraint_kwargs: Dict[str, bool],
        sql: str
    ) -> None: ...
    @classmethod
    def _digest(cls, *args) -> str: ...
    def _field_indexes_sql(
        self,
        model: Any,
        field: Field
    ) -> List[Statement]: ...