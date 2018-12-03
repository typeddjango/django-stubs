from typing import Any

from .utils import (
    ProgrammingError as ProgrammingError,
    IntegrityError as IntegrityError,
    OperationalError as OperationalError,
    DatabaseError as DatabaseError,
    DataError as DataError,
    NotSupportedError as NotSupportedError,
)

connections: Any
router: Any

class DefaultConnectionProxy:
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...

connection: Any
