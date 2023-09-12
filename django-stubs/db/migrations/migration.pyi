from collections.abc import Sequence
from typing import ClassVar

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState
from typing_extensions import Self

class Migration:
    # Django copies these 4 attributes from the class to the instance,
    # but they're practically used as ClassVar
    operations: ClassVar[Sequence[Operation]]
    dependencies: ClassVar[list[tuple[str, str]]]
    run_before: ClassVar[list[tuple[str, str]]]
    replaces: ClassVar[list[tuple[str, str]]]
    initial: ClassVar[bool | None]
    atomic: ClassVar[bool]
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
    def __new__(cls, value: tuple[str, str], setting: str) -> Self: ...

def swappable_dependency(value: str) -> SwappableTuple: ...
