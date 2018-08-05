from typing import Any, Callable, List, Optional, Set, Tuple, Union

from django.db import DefaultConnectionProxy
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.migration import Migration
from django.db.migrations.state import ProjectState

from .exceptions import InvalidMigrationPlan
from .loader import MigrationLoader
from .recorder import MigrationRecorder
from .state import ProjectState


class MigrationExecutor:
    connection: django.db.backends.sqlite3.base.DatabaseWrapper = ...
    loader: django.db.migrations.loader.MigrationLoader = ...
    recorder: django.db.migrations.recorder.MigrationRecorder = ...
    progress_callback: Callable = ...
    def __init__(
        self,
        connection: Optional[
            Union[
                DefaultConnectionProxy, backends.base.base.BaseDatabaseWrapper
            ]
        ],
        progress_callback: Optional[Callable] = ...,
    ) -> None: ...
    def migration_plan(
        self,
        targets: Union[
            Set[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, None]]
        ],
        clean_start: bool = ...,
    ) -> Union[List[Tuple[Migration, bool]], List[Tuple[Any, bool]]]: ...
    def migrate(
        self,
        targets: Optional[Union[List[Tuple[str, str]], List[Tuple[str, None]]]],
        plan: Optional[List[Tuple[Migration, bool]]] = ...,
        state: Optional[ProjectState] = ...,
        fake: bool = ...,
        fake_initial: bool = ...,
    ) -> ProjectState: ...
    def collect_sql(self, plan: List[Tuple[Migration, bool]]) -> List[str]: ...
    def apply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...,
        fake_initial: bool = ...,
    ) -> ProjectState: ...
    def unapply_migration(
        self, state: ProjectState, migration: Migration, fake: bool = ...
    ) -> ProjectState: ...
    def check_replacements(self) -> None: ...
    def detect_soft_applied(
        self, project_state: Optional[ProjectState], migration: Migration
    ) -> Tuple[bool, ProjectState]: ...
