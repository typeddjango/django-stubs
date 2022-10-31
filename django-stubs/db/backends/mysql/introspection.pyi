from collections import namedtuple
from typing import Any

from django.db.backends.base.introspection import BaseDatabaseIntrospection as BaseDatabaseIntrospection
from django.db.backends.mysql.base import DatabaseWrapper

FieldInfo: Any
InfoLine = namedtuple(
    "InfoLine",
    [
        "col_name",
        "data_type",
        "max_len",
        "num_prec",
        "num_scale",
        "extra",
        "column_default",
        "collation",
        "is_unsigned",
    ],
)

class DatabaseIntrospection(BaseDatabaseIntrospection):
    connection: DatabaseWrapper
    data_types_reverse: Any = ...
    def get_field_type(self, data_type: Any, description: Any) -> Any: ...
    def get_table_list(self, cursor: Any) -> Any: ...
    def get_table_description(self, cursor: Any, table_name: Any) -> Any: ...
    def get_sequences(self, cursor: Any, table_name: Any, table_fields: Any = ...) -> Any: ...
    def get_relations(self, cursor: Any, table_name: Any) -> Any: ...
    def get_key_columns(self, cursor: Any, table_name: Any) -> Any: ...
    def get_storage_engine(self, cursor: Any, table_name: Any) -> Any: ...
    def get_constraints(self, cursor: Any, table_name: Any) -> Any: ...
