from typing import Dict


def _escape_pgpass(txt: str) -> str: ...


class DatabaseClient:
    @classmethod
    def runshell_db(cls, conn_params: Dict[str, str]) -> None: ...