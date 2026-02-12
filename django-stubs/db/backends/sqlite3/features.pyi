from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.utils.functional import cached_property

class DatabaseFeatures(BaseDatabaseFeatures):
    connection: DatabaseWrapper
    can_alter_table_drop_column: bool
    supports_aggregate_order_by_clause: bool
    supports_aggregate_distinct_multiple_argument: bool
    supports_any_value: bool
    @cached_property
    def django_test_skips(self) -> dict[str, set[str]]: ...  # type: ignore[override]
    @cached_property
    def introspected_field_types(self) -> dict[str, str]: ...  # type: ignore[override]
    @property
    def max_query_params(self) -> int: ...  # type: ignore[override]
    @cached_property
    def supports_json_field(self) -> bool: ...  # type: ignore[override]
    @property
    def can_introspect_json_field(self) -> bool: ...  # type: ignore[override]
    @property
    def has_json_object_function(self) -> bool: ...  # type: ignore[override]
    @cached_property
    def can_return_columns_from_insert(self) -> bool: ...  # type: ignore[override]
    @property
    def can_return_rows_from_bulk_insert(self) -> bool: ...  # type: ignore[override]
    @property
    def can_return_rows_from_update(self) -> bool: ...  # type: ignore[override]
