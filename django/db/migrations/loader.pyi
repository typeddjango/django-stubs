from django.db import DefaultConnectionProxy
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.migrations.migration import (
    Migration,
    SwappableTuple,
)
from django.db.migrations.state import ProjectState
from typing import (
    Dict,
    Optional,
    Set,
    Tuple,
    Union,
)


class MigrationLoader:
    def __init__(
        self,
        connection: Optional[Union[DefaultConnectionProxy, backends.sqlite3.base.DatabaseWrapper]],
        load: bool = ...,
        ignore_no_migrations: bool = ...
    ) -> None: ...
    def add_external_dependencies(
        self,
        key: Tuple[str, str],
        migration: Migration
    ) -> None: ...
    def add_internal_dependencies(
        self,
        key: Tuple[str, str],
        migration: Migration
    ) -> None: ...
    def build_graph(self) -> None: ...
    def check_consistent_history(
        self,
        connection: Union[DefaultConnectionProxy, backends.sqlite3.base.DatabaseWrapper]
    ) -> None: ...
    def check_key(
        self,
        key: Union[SwappableTuple, Tuple[str, str]],
        current_app: str
    ) -> Optional[Tuple[str, str]]: ...
    def detect_conflicts(self) -> Dict[str, Set[str]]: ...
    def get_migration(self, app_label: str, name_prefix: str) -> Migration: ...
    def get_migration_by_prefix(self, app_label: str, name_prefix: str) -> Migration: ...
    def load_disk(self) -> None: ...
    @classmethod
    def migrations_module(cls, app_label: str) -> Union[Tuple[None, bool], Tuple[str, bool]]: ...
    def project_state(
        self,
        nodes: Optional[Tuple[str, str]] = ...,
        at_end: bool = ...
    ) -> ProjectState: ...