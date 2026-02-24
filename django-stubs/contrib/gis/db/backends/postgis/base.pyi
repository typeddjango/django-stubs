from typing import Any

from django.db.backends.postgresql.base import DatabaseWrapper as Psycopg2DatabaseWrapper
from psycopg import BaseConnection
from psycopg.adapt import Dumper
from psycopg.pq import Format

class BaseBinaryDumper(Dumper):
    format: Format
    def dump(self, obj: Any) -> bytes: ...

class BaseTextDumper(Dumper):
    def dump(self, obj: Any) -> bytes: ...

class RsterType: ...

class DatabaseWrapper(Psycopg2DatabaseWrapper):
    SchemaEditorClass: Any
    features: Any
    ops: Any
    introspection: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def prepare_database(self) -> None: ...
    def register_geometry_adapters(self, pg_connection: BaseConnection[bytes], clear_caches: bool = False) -> None: ...
