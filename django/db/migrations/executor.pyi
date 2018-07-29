from django.db import DefaultConnectionProxy
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.migration import Migration
from django.db.migrations.state import ProjectState
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


class MigrationExecutor:
    def __init__(
        self,
        connection: Optional[Union[DefaultConnectionProxy, backends.base.base.BaseDatabaseWrapper]],
        progress_callback: Optional[Callable] = ...
    ) -> None: ...
    def _create_project_state(self, with_applied_migrations: bool = ...) -> ProjectState: ...
    def _migrate_all_backwards(self, plan: Any, full_plan: Any, fake: bool) -> ProjectState: ...
    def _migrate_all_forwards(
        self,
        state: ProjectState,
        plan: Any,
        full_plan: Any,
        fake: bool,
        fake_initial: bool
    ) -> ProjectState: ...
    def apply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...,
        fake_initial: bool = ...
    ) -> ProjectState: ...
    def check_replacements(self) -> None: ...
    def detect_soft_applied(
        self,
        project_state: None,
        migration: Migration
    ) -> Tuple[bool, ProjectState]: ...
    def migrate(
        self,
        targets: Optional[Union[List[Tuple[str, str]], List[Tuple[str, None]]]],
        plan: Any = ...,
        state: Optional[ProjectState] = ...,
        fake: bool = ...,
        fake_initial: bool = ...
    ) -> ProjectState: ...
    def migration_plan(
        self,
        targets: Union[Set[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, None]]],
        clean_start: bool = ...
    ) -> Any: ...
    def unapply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...
    ) -> ProjectState: ...