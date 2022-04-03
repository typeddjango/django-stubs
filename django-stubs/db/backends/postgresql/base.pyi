from io import IOBase
from typing import Any, Dict, Tuple, Type

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorDebugWrapper as BaseCursorDebugWrapper

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations

def psycopg2_version() -> Tuple[int, ...]: ...

PSYCOPG2_VERSION: Tuple[int, ...] = ...

class DatabaseWrapper(BaseDatabaseWrapper):
    client: DatabaseClient
    creation: DatabaseCreation
    features: DatabaseFeatures
    introspection: DatabaseIntrospection
    ops: DatabaseOperations

    client_class: Type[DatabaseClient]
    creation_class: Type[DatabaseCreation]
    features_class: Type[DatabaseFeatures]
    introspection_class: Type[DatabaseIntrospection]
    ops_class: Type[DatabaseOperations]

    operators: Dict[str, str] = ...
    pattern_esc: str = ...
    pattern_ops: Dict[str, str] = ...

    # PostgreSQL backend-specific attributes.
    _named_cursor_idx: int = ...
    @property
    def pg_version(self) -> int: ...

class CursorDebugWrapper(BaseCursorDebugWrapper):
    def copy_expert(self, sql: str, file: IOBase, *args: Any): ...
    def copy_to(self, file: IOBase, table: str, *args: Any, **kwargs: Any): ...
