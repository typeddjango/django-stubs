from typing import Any, Dict, List, Optional

from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    executable_name: str = ...
    @classmethod
    def settings_to_cmd_args(
        cls, settings_dict: Dict[str, Any]
    ) -> List[str]: ...
    def runshell(self) -> None: ...
