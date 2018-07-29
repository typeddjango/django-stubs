from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.operations.fields import AddField
from django.db.migrations.operations.models import (
    CreateModel,
    ModelOperation,
)
from django.db.migrations.state import (
    ProjectState,
    StateApps,
)
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Union,
)


class RunPython:
    def __init__(
        self,
        code: Union[str, Callable],
        reverse_code: Optional[Callable] = ...,
        atomic: None = ...,
        hints: Optional[Dict[str, str]] = ...,
        elidable: bool = ...
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
    def describe(self) -> str: ...
    @staticmethod
    def noop(
        apps: StateApps,
        schema_editor: DatabaseSchemaEditor
    ) -> None: ...
    @property
    def reversible(self) -> bool: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...


class RunSQL:
    def _run_sql(
        self,
        schema_editor: DatabaseSchemaEditor,
        sqls: Union[str, List[str]]
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


class SeparateDatabaseAndState:
    def __init__(
        self,
        database_operations: List[ModelOperation] = ...,
        state_operations: Union[List[CreateModel], List[AddField], List[ModelOperation]] = ...
    ) -> None: ...
    def database_forwards(
        self,
        app_label: str,
        schema_editor: DatabaseSchemaEditor,
        from_state: ProjectState,
        to_state: ProjectState
    ) -> None: ...
    def state_forwards(self, app_label: str, state: ProjectState) -> None: ...