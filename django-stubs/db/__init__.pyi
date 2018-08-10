from collections import deque
from typing import Any, Callable, Dict, List, Optional, Union
from unittest.mock import MagicMock

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.backends.sqlite3.creation import DatabaseCreation
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.db.backends.sqlite3.introspection import DatabaseIntrospection
from django.db.backends.sqlite3.operations import DatabaseOperations
from django.db.utils import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS
from django.db.utils import \
    DJANGO_VERSION_PICKLE_KEY as DJANGO_VERSION_PICKLE_KEY
from django.db.utils import DatabaseError as DatabaseError
from django.db.utils import DataError as DataError
from django.db.utils import Error as Error
from django.db.utils import IntegrityError as IntegrityError
from django.db.utils import InterfaceError as InterfaceError
from django.db.utils import InternalError as InternalError
from django.db.utils import NotSupportedError as NotSupportedError
from django.db.utils import OperationalError as OperationalError
from django.db.utils import ProgrammingError as ProgrammingError

connections: Any
router: Any

class DefaultConnectionProxy:
    def __getattr__(
        self, item: str
    ) -> Union[
        Callable,
        Dict[str, Optional[Union[Dict[Any, Any], Dict[str, None], int, str]]],
        List[Dict[str, str]],
        List[str],
        bool,
        deque,
        DatabaseCreation,
        DatabaseFeatures,
        DatabaseIntrospection,
        DatabaseOperations,
        str,
    ]: ...
    def __setattr__(self, name: str, value: Union[bool, MagicMock]) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __eq__(self, other: DatabaseWrapper) -> bool: ...

connection: Any
