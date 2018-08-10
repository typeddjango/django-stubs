from typing import Callable, List, Optional, Set, Tuple, Union

from django.contrib.admin.migrations.0001_initial import Migration
from django.contrib.admin.migrations.0002_logentry_remove_auto_add import \
    Migration
from django.contrib.admin.migrations.0003_logentry_add_action_flag_choices import \
    Migration
from django.contrib.sites.migrations.0001_initial import Migration
from django.contrib.sites.migrations.0002_alter_domain_unique import Migration
from django.db import DefaultConnectionProxy
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.migration import Migration
from django.db.migrations.state import ProjectState


class MigrationExecutor:
    connection: django.db.backends.sqlite3.base.DatabaseWrapper
    loader: django.db.migrations.loader.MigrationLoader
    progress_callback: Callable
    recorder: django.db.migrations.recorder.MigrationRecorder

    def __init__(
        self,
        connection: Optional[Union[DefaultConnectionProxy, BaseDatabaseWrapper]],
        progress_callback: Optional[Callable] = ...
    ) -> None: ...
    def apply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...,
        fake_initial: bool = ...
    ) -> ProjectState: ...
    def check_replacements(self) -> None: ...
    def collect_sql(self, plan: List[Tuple[Migration, bool]]) -> List[str]: ...
    def detect_soft_applied(
        self,
        project_state: Optional[ProjectState],
        migration: Migration
    ) -> Tuple[bool, ProjectState]: ...
    def migrate(
        self,
        targets: Optional[List[Tuple[str, Optional[str]]]],
        plan: Optional[List[Union[Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool], Tuple[Migration, bool]]]] = ...,
        state: Optional[ProjectState] = ...,
        fake: bool = ...,
        fake_initial: bool = ...
    ) -> ProjectState: ...
    def migration_plan(
        self,
        targets: Union[List[Tuple[str, Optional[str]]], Set[Tuple[str, str]]],
        clean_start: bool = ...
    ) -> List[Tuple[bool, bool]]: ...
    def unapply_migration(
        self,
        state: ProjectState,
        migration: Migration,
        fake: bool = ...
    ) -> ProjectState: ...
