from _typeshed import Self
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState

class Migration:
    operations: list[Operation]
    dependencies: list[tuple[str, str]]
    run_before: list[tuple[str, str]]
    replaces: list[tuple[str, str]]
    initial: bool | None
    atomic: bool
    name: str
    app_label: str
    def __init__(self, name: str, app_label: str) -> None: ...
    def mutate_state(self, project_state: ProjectState, preserve: bool = ...) -> ProjectState: ...
    def apply(
        self, project_state: ProjectState, schema_editor: BaseDatabaseSchemaEditor, collect_sql: bool = ...
    ) -> ProjectState: ...
    def unapply(
        self, project_state: ProjectState, schema_editor: BaseDatabaseSchemaEditor, collect_sql: bool = ...
    ) -> ProjectState: ...

class SwappableTuple(tuple[str, str]):
    setting: str
    def __new__(cls: type[Self], value: tuple[str, str], setting: str) -> Self: ...

def swappable_dependency(value: str) -> SwappableTuple: ...
