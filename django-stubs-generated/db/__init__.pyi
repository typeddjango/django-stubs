from typing import Any, Optional, Union
from unittest.mock import MagicMock

from django.db.backends.sqlite3.base import DatabaseWrapper
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
    def __getattr__(self, item: str) -> Any: ...
    def __setattr__(self, name: str, value: Union[bool, MagicMock]) -> None: ...
    def __delattr__(self, name: str) -> None: ...

connection: Any
