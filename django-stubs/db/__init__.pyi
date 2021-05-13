from typing import Any

from .backends.base.base import BaseDatabaseWrapper
from .utils import (
    DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS,
    DJANGO_VERSION_PICKLE_KEY as DJANGO_VERSION_PICKLE_KEY,
    ProgrammingError as ProgrammingError,
    IntegrityError as IntegrityError,
    OperationalError as OperationalError,
    DatabaseError as DatabaseError,
    DataError as DataError,
    NotSupportedError as NotSupportedError,
    InternalError as InternalError,
    InterfaceError as InterfaceError,
    Error as Error,
    ConnectionDoesNotExist as ConnectionDoesNotExist,
    # Not exported in __all__
    ConnectionHandler,
    ConnectionRouter,
)

from . import migrations

connections: ConnectionHandler
router: ConnectionRouter
# Actually DefaultConnectionProxy, but quacks exactly like BaseDatabaseWrapper, it's not worth distinguishing the two.
connection: BaseDatabaseWrapper

class DefaultConnectionProxy:
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...

def close_old_connections(**kwargs: Any) -> None: ...
def reset_queries(**kwargs: Any) -> None: ...
