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
    def _migrate_all_backwards(
        self,
        plan: List[Tuple[Migration, bool]],
        full_plan: Union[List[Any], List[Tuple[Migration, bool]]],
        fake: bool
    ) -> ProjectState: ...
    def _migrate_all_forwards(
        self,
        state: ProjectState,
        plan: Union[List[Any], List[Tuple[Migration, bool]]],
        full_plan: Union[List[Any], List[Tuple[Migration, bool]]],
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
        targets: Optional[Union[List[Tuple[str, None]], List[Tuple[str, str]]]],
        plan: Optional[Union[List[Any], List[Tuple[Migration, bool]]]] = ...,
        state: Optional[ProjectState] = ...,
        fake: bool = ...,
        fake_initial: bool = ...
    ) -> ProjectState: ...
    def migration_plan(
        self,
        targets: Union[List[Tuple[str, None]], List[Tuple[str, str]], Set[Tuple[str, str]]],
        clean_start: bool = ...
    ) -> Union[List[Any], List[Tuple[Migration, bool]], List[Tuple[object, bool]]]: ...
    def unapply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...
    ) -> ProjectState: ...