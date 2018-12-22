from typing import Any, Optional, Tuple

from django.db.backends.base.creation import BaseDatabaseCreation

class DatabaseCreation(BaseDatabaseCreation):
    connection: Any
    @staticmethod
    def is_in_memory_db(database_name: str) -> bool: ...
    def get_test_db_clone_settings(self, suffix: Any): ...
    def test_db_signature(self) -> Tuple[str, str]: ...
