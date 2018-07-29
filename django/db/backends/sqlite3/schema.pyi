from django.db.models.base import Model
from django.db.models.fields import (
    AutoField,
    Field,
    IntegerField,
    SlugField,
    TimeField,
)
from typing import (
    Any,
    Dict,
    Optional,
    Type,
    Union,
)


class DatabaseSchemaEditor:
    def __enter__(self) -> DatabaseSchemaEditor: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...
    def _alter_field(
        self,
        model: Any,
        old_field: Field,
        new_field: Field,
        old_type: str,
        new_type: str,
        old_db_params: Dict[str, Union[str, None]],
        new_db_params: Dict[str, Union[str, None]],
        strict: bool = ...
    ) -> None: ...
    def _is_referenced_by_fk_constraint(
        self,
        table_name: str,
        column_name: Optional[str] = ...,
        ignore_self: bool = ...
    ) -> bool: ...
    def _remake_table(
        self,
        model: Any,
        create_field: Optional[Union[IntegerField, TimeField]] = ...,
        delete_field: Optional[Union[AutoField, SlugField]] = ...,
        alter_field: Any = ...
    ) -> None: ...
    def add_field(self, model: Type[Model], field: Field) -> None: ...
    def alter_db_table(
        self,
        model: Any,
        old_db_table: str,
        new_db_table: str,
        disable_constraints: bool = ...
    ) -> None: ...
    def alter_field(
        self,
        model: Any,
        old_field: Field,
        new_field: Field,
        strict: bool = ...
    ) -> None: ...
    def delete_model(self, model: Any, handle_autom2m: bool = ...) -> None: ...
    def quote_value(self, value: Optional[Union[int, memoryview, str]]) -> str: ...
    def remove_field(self, model: Type[Model], field: Field) -> None: ...