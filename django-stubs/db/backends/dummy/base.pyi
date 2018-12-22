from typing import Any, Optional

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations

def complain(*args: Any, **kwargs: Any) -> Any: ...
def ignore(*args: Any, **kwargs: Any) -> None: ...

class DatabaseOperations(BaseDatabaseOperations):
    connection: django.db.backends.dummy.base.DatabaseWrapper
    quote_name: Any = ...

class DatabaseClient(BaseDatabaseClient):
    connection: django.db.backends.dummy.base.DatabaseWrapper
    runshell: Any = ...

class DatabaseCreation(BaseDatabaseCreation):
    connection: django.db.backends.dummy.base.DatabaseWrapper
    create_test_db: Any = ...
    destroy_test_db: Any = ...

class DatabaseIntrospection(BaseDatabaseIntrospection):
    connection: django.db.backends.dummy.base.DatabaseWrapper
    get_table_list: Any = ...
    get_table_description: Any = ...
    get_relations: Any = ...
    get_indexes: Any = ...
    get_key_columns: Any = ...

class DatabaseWrapper(BaseDatabaseWrapper):
    alias: str
    allow_thread_sharing: bool
    autocommit: bool
    client: django.db.backends.dummy.base.DatabaseClient
    close_at: None
    closed_in_transaction: bool
    commit_on_exit: bool
    connection: None
    creation: django.db.backends.dummy.base.DatabaseCreation
    errors_occurred: bool
    execute_wrappers: List[Any]
    features: django.db.backends.dummy.features.DummyDatabaseFeatures
    force_debug_cursor: bool
    in_atomic_block: bool
    introspection: django.db.backends.dummy.base.DatabaseIntrospection
    needs_rollback: bool
    ops: django.db.backends.dummy.base.DatabaseOperations
    queries_log: collections.deque
    run_commit_hooks_on_set_autocommit_on: bool
    run_on_commit: List[Any]
    savepoint_ids: List[Any]
    savepoint_state: int
    settings_dict: Dict[str, Optional[Union[Dict[str, None], int, str]]]
    validation: django.db.backends.base.validation.BaseDatabaseValidation
    operators: Any = ...
    ensure_connection: Any = ...
    client_class: Any = ...
    creation_class: Any = ...
    features_class: Any = ...
    introspection_class: Any = ...
    ops_class: Any = ...
    def is_usable(self): ...
