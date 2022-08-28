from typing import Any, Dict, Optional, Sequence, Set, Tuple, Type

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.base import Model
from django.db.utils import DatabaseError

class BaseDatabaseFeatures:
    minimum_database_version: Optional[Tuple[int, ...]]
    gis_enabled: bool
    allows_group_by_lob: bool
    allows_group_by_pk: bool
    allows_group_by_selected_pks: bool
    empty_fetchmany_value: Sequence[Any]
    update_can_self_select: bool
    interprets_empty_strings_as_nulls: bool
    supports_nullable_unique_constraints: bool
    supports_partially_nullable_unique_constraints: bool
    supports_deferrable_unique_constraints: bool
    can_use_chunked_reads: bool
    can_return_columns_from_insert: bool
    can_return_rows_from_bulk_insert: bool
    has_bulk_insert: bool
    uses_savepoints: bool
    can_release_savepoints: bool
    related_fields_match_type: bool
    allow_sliced_subqueries_with_in: bool
    has_select_for_update: bool
    has_select_for_update_nowait: bool
    has_select_for_update_skip_locked: bool
    has_select_for_update_of: bool
    has_select_for_no_key_update: bool
    select_for_update_of_column: bool
    test_db_allows_multiple_connections: bool
    supports_unspecified_pk: bool
    supports_forward_references: bool
    truncates_names: bool
    has_real_datatype: bool
    supports_subqueries_in_group_by: bool
    has_native_uuid_field: bool
    has_native_duration_field: bool
    supports_temporal_subtraction: bool
    supports_regex_backreferencing: bool
    supports_date_lookup_using_string: bool
    supports_timezones: bool
    has_zoneinfo_database: bool
    requires_explicit_null_ordering_when_grouping: bool
    nulls_order_largest: bool
    supports_order_by_nulls_modifier: bool
    order_by_nulls_first: bool
    max_query_params: Optional[int]
    allows_auto_pk_0: bool
    can_defer_constraint_checks: bool
    supports_tablespaces: bool
    supports_sequence_reset: bool
    can_introspect_default: bool
    can_introspect_foreign_keys: bool
    introspected_field_types: Dict[str, str]
    supports_index_column_ordering: bool
    can_introspect_materialized_views: bool
    can_distinct_on_fields: bool
    atomic_transactions: bool
    can_rollback_ddl: bool
    supports_atomic_references_rename: bool
    supports_combined_alters: bool
    supports_foreign_keys: bool
    can_create_inline_fk: bool
    can_rename_index: bool
    indexes_foreign_keys: bool
    supports_column_check_constraints: bool
    supports_table_check_constraints: bool
    can_introspect_check_constraints: bool
    supports_paramstyle_pyformat: bool
    requires_literal_defaults: bool
    connection_persists_old_columns: bool
    closed_cursor_error_class: Type[DatabaseError]
    has_case_insensitive_like: bool
    bare_select_suffix: str
    implied_column_null: bool
    supports_select_for_update_with_limit: bool
    greatest_least_ignores_nulls: bool
    can_clone_databases: bool
    ignores_table_name_case: bool
    for_update_after_from: bool
    supports_select_union: bool
    supports_select_intersection: bool
    supports_select_difference: bool
    supports_slicing_ordering_in_compound: bool
    supports_parentheses_in_compound: bool
    supports_aggregate_filter_clause: bool
    supports_index_on_text_field: bool
    supports_over_clause: bool
    supports_frame_range_fixed_distance: bool
    only_supports_unbounded_with_preceding_and_following: bool
    supports_cast_with_precision: bool
    time_cast_precision: int
    create_test_procedure_without_params_sql: Optional[str]
    create_test_procedure_with_int_param_sql: Optional[str]
    supports_callproc_kwargs: bool
    supported_explain_formats: Set[str]
    supports_default_in_lead_lag: bool
    supports_ignore_conflicts: bool
    supports_update_conflicts: bool
    supports_update_conflicts_with_target: bool
    requires_casted_case_in_updates: bool
    supports_partial_indexes: bool
    supports_functions_in_partial_indexes: bool
    supports_covering_indexes: bool
    supports_expression_indexes: bool
    collate_as_index_expression: bool
    allows_multiple_constraints_on_same_fields: bool
    supports_boolean_expr_in_select_clause: bool
    supports_json_field: bool
    can_introspect_json_field: bool
    supports_primitives_in_json_field: bool
    has_native_json_field: bool
    has_json_operators: bool
    supports_json_field_contains: bool
    json_key_contains_list_matching_requires_list: bool
    has_json_object_function: bool
    supports_collation_on_charfield: bool
    supports_collation_on_textfield: bool
    supports_non_deterministic_collations: bool
    test_collations: Dict[str, Optional[str]]
    test_now_utc_template: Optional[str]
    django_test_expected_failures: Set[str]
    django_test_skips: Dict[str, Set[str]]
    connection: BaseDatabaseWrapper
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...
    @property
    def supports_explaining_query_execution(self) -> bool: ...
    @property
    def supports_transactions(self) -> bool: ...
    def allows_group_by_selected_pks_on_model(self, model: Type[Model]) -> bool: ...
