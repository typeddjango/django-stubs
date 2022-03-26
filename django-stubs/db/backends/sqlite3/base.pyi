from sqlite3 import dbapi2 as Database
from typing import Any, Callable, Type, TypeVar

from django.db.backends.base.base import BaseDatabaseWrapper

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations

_R = TypeVar("_R")

def decoder(conv_func: Callable[[str], _R]) -> Callable[[bytes], _R]: ...

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

FORMAT_QMARK_REGEX: Any

class SQLiteCursorWrapper(Database.Cursor): ...

def check_sqlite_version() -> None: ...
