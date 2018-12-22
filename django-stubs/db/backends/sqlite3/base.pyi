from sqlite3 import dbapi2 as Database
from sqlite3 import dbapi2 as Database
from typing import Any, Callable, Iterator

from django.db.backends.base.base import BaseDatabaseWrapper

def decoder(conv_func: Callable) -> Callable: ...

class DatabaseWrapper(BaseDatabaseWrapper): ...

FORMAT_QMARK_REGEX: Any

class SQLiteCursorWrapper(Database.Cursor): ...
