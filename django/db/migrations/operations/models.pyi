from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.operations.fields import FieldOperation
from django.db.migrations.state import ProjectState
from django.db.models.indexes import Index
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


def _check_for_duplicates(arg_name: str, objs: Iterator[Any]) -> None: ...


class AddIndex:
    def __init__(self, model_name: str, index: Index) -> None: ...
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
    def describe(self) -> str: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class AlterIndexTogether:
    def __init__(
        self,
        name: str,
        index_together: Optional[Union[List[List[str]], List[Tuple[str, str]], Set[Tuple[str, str]]]]
    ) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, Union[str, Set[Tuple[str, str]]]]]: ...
    def references_field(self, model_name: str, name: str, app_label: None = ...) -> bool: ...


class AlterModelManagers:
    def __init__(self, name: str, managers: List[Any]) -> None: ...
    def describe(self) -> str: ...


class AlterModelOptions:
    def __init__(self, name: str, options: Dict[str, Union[List[Tuple[str, str]], str]]) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, Union[str, Dict[str, List[Tuple[str, str]]]]]]: ...


class AlterModelTable:
    def __init__(self, name: str, table: str) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, str]]: ...
    def describe(self) -> str: ...
    def reduce(
        self,
        operation: DeleteModel,
        in_between: List[Any],
        app_label: None = ...
    ) -> List[DeleteModel]: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class AlterOrderWithRespectTo:
    def __init__(self, name: str, order_with_respect_to: str) -> None: ...
    def database_backwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, str]]: ...
    def describe(self) -> str: ...
    def references_field(self, model_name: str, name: str, app_label: None = ...) -> bool: ...


class AlterUniqueTogether:
    def __init__(
        self,
        name: str,
        unique_together: Optional[Union[List[List[str]], Set[Tuple[str, str]], List[Tuple[str, str]]]]
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
    def deconstruct(self) -> Tuple[str, List[Any], Dict[str, Union[str, Set[Tuple[str, str]]]]]: ...
    def describe(self) -> str: ...
    def references_field(self, model_name: str, name: str, app_label: Optional[str] = ...) -> bool: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class CreateModel:
    def __init__(
        self,
        name: str,
        fields: Any,
        options: Any = ...,
        bases: Any = ...,
        managers: Any = ...
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
    def model_to_key(self, model: str) -> List[str]: ...
    def reduce(
        self,
        operation: Operation,
        in_between: Any,
        app_label: Optional[str] = ...
    ) -> Union[bool, List[CreateModel]]: ...
    def references_model(self, name: str, app_label: Optional[str] = ...) -> bool: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class DeleteModel:
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


class FieldRelatedOptionOperation:
    def reduce(
        self,
        operation: Union[FieldOperation, CreateModel, AlterIndexTogether],
        in_between: List[DeleteModel],
        app_label: Optional[str] = ...
    ) -> Any: ...


class IndexOperation:
    @cached_property
    def model_name_lower(self) -> str: ...


class ModelOperation:
    def __init__(self, name: str) -> None: ...
    @cached_property
    def name_lower(self) -> str: ...
    def reduce(
        self,
        operation: Union[FieldOperation, ModelOperation],
        in_between: Any,
        app_label: Optional[str] = ...
    ) -> bool: ...
    def references_model(self, name: str, app_label: Optional[str] = ...) -> bool: ...


class ModelOptionOperation:
    def reduce(
        self,
        operation: Union[FieldOperation, CreateModel, FieldRelatedOptionOperation],
        in_between: List[DeleteModel],
        app_label: Optional[str] = ...
    ) -> Union[bool, List[AlterUniqueTogether]]: ...


class RemoveIndex:
    def __init__(self, model_name: str, name: str) -> None: ...
    def database_backwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class RenameModel:
    def __init__(self, old_name: str, new_name: str) -> None: ...
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
    @cached_property
    def new_name_lower(self) -> str: ...
    @cached_property
    def old_name_lower(self) -> str: ...
    def reduce(
        self,
        operation: AlterModelTable,
        in_between: List[Any],
        app_label: str = ...
    ) -> bool: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...