from typing import Any, Dict, Iterable, List, Tuple

from django.db.backends.base.client import BaseDatabaseClient as BaseDatabaseClient
from django.db.backends.oracle.base import DatabaseWrapper

class DatabaseClient(BaseDatabaseClient):
    connection: DatabaseWrapper
    executable_name: str = ...
    wrapper_name: str = ...
    @staticmethod
    def connect_string(settings_dict: Dict[str, Any]) -> str: ...
    @classmethod
    def settings_to_cmd_args_env(
        cls, settings_dict: Dict[str, Any], parameters: Iterable[str]
    ) -> Tuple[List[str], None]: ...
