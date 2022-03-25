from typing import Any, Dict, Iterable, Optional, Sequence, Tuple

from django.db.backends.base.base import BaseDatabaseWrapper

class BaseDatabaseClient:
    executable_name: Optional[str] = ...
    connection: BaseDatabaseWrapper
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...
    @classmethod
    def settings_to_cmd_args_env(
        cls,
        settings_dict: Dict[str, Any],
        parameters: Iterable[str],
    ) -> Tuple[Sequence[str], Optional[Dict[str, str]]]: ...
    def runshell(self, parameters: Iterable[str]) -> None: ...
