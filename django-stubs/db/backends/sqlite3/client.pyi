from typing import Any, Dict, Iterable, List, Tuple

from django.db.backends.base.client import BaseDatabaseClient as BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    executable_name: str = ...
    @classmethod
    def settings_to_cmd_args_env(
        self, settings_dict: Dict[str, Any], parameters: Iterable[str]
    ) -> Tuple[List[str], None]: ...
