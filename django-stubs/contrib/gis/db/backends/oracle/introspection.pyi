from functools import cached_property
from typing import Any

from django.db.backends.oracle.introspection import DatabaseIntrospection

class OracleIntrospection(DatabaseIntrospection):
    @cached_property
    def data_types_reverse(self) -> dict[int, str]: ...  # type: ignore[override]
    def get_geometry_type(self, table_name: Any, description: Any) -> Any: ...
