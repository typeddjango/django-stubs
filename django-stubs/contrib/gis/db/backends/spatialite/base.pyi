from typing import Any

from django.contrib.gis.db.backends.spatialite.operations import SpatiaLiteOperations
from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper

class DatabaseWrapper(SQLiteDatabaseWrapper):
    SchemaEditorClass: Any
    client_class: Any
    features_class: Any
    introspection_class: Any
    ops_class: Any
    lib_spatialite_paths: Any
    ops: SpatiaLiteOperations
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_new_connection(self, conn_params: Any) -> Any: ...
    def prepare_database(self) -> None: ...
