from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.operations.models import (
    AlterUniqueTogether,
    CreateModel,
    DeleteModel,
    FieldRelatedOptionOperation,
    ModelOperation,
)
from django.db.migrations.state import ProjectState
from django.db.models.fields import (
    CharField,
    Field,
    IntegerField,
    SlugField,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


class AddField:
    def __init__(
        self,
        model_name: str,
        name: str,
        field: Field,
        preserve_default: bool = ...
    ) -> None: ...
    def database_backwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(self) -> Any: ...
    def describe(self) -> str: ...
    def reduce(
        self,
        operation: Union[FieldOperation, CreateModel, FieldRelatedOptionOperation],
        in_between: List[AddField],
        app_label: Optional[str] = ...
    ) -> Union[bool, List[AddField]]: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class AlterField:
    def __init__(
        self,
        model_name: str,
        name: str,
        field: Field,
        preserve_default: bool = ...
    ) -> None: ...
    def database_backwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(
        self
    ) -> Union[Tuple[str, List[Any], Dict[str, Union[str, SlugField]]], Tuple[str, List[Any], Dict[str, Union[str, CharField]]], Tuple[str, List[Any], Dict[str, Union[str, IntegerField]]]]: ...
    def describe(self) -> str: ...
    def reduce(
        self,
        operation: Union[AlterField, DeleteModel, AlterUniqueTogether],
        in_between: List[Any],
        app_label: str = ...
    ) -> bool: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class FieldOperation:
    def __init__(self, model_name: str, name: str) -> None: ...
    def is_same_field_operation(self, operation: FieldOperation) -> bool: ...
    def is_same_model_operation(self, operation: FieldOperation) -> bool: ...
    @cached_property
    def model_name_lower(self) -> str: ...
    @cached_property
    def name_lower(self) -> str: ...
    def reduce(
        self,
        operation: Union[ModelOperation, FieldOperation],
        in_between: Any,
        app_label: str = ...
    ) -> bool: ...
    def references_field(self, model_name: str, name: str, app_label: Optional[str] = ...) -> bool: ...
    def references_model(self, name: str, app_label: Optional[str] = ...) -> bool: ...


class RemoveField:
    def database_backwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, str]]: ...
    def describe(self) -> str: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class RenameField:
    def __init__(self, model_name: str, old_name: str, new_name: str) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, str]]: ...
    @cached_property
    def old_name_lower(self) -> str: ...
    def reduce(
        self,
        operation: Union[FieldOperation, AlterUniqueTogether],
        in_between: List[Any],
        app_label: Optional[str] = ...
    ) -> Union[bool, List[RenameField]]: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...