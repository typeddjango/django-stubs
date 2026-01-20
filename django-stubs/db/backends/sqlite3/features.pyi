from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.sqlite3.base import DatabaseWrapper

class DatabaseFeatures(BaseDatabaseFeatures):
    connection: DatabaseWrapper
    can_return_rows_from_update: bool
    supports_aggregate_order_by_clause: bool
    supports_aggregate_distinct_multiple_argument: bool
    supports_any_value: bool
    @property
    def max_query_params(self) -> int: ...  # type: ignore[override]
