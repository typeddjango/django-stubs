from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from django.db.backends.base.client import BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    executable_name: str = ...
    @classmethod
    def settings_to_cmd_args_env(
        self, settings_dict: Dict[str, Any], parameters: Iterable[str]
    ) -> Tuple[List[str], Optional[Dict[str, str]]]: ...
