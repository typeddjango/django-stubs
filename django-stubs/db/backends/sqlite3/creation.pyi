from os import PathLike
from typing import Union

from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.sqlite3.base import DatabaseWrapper

class DatabaseCreation(BaseDatabaseCreation):
    connection: DatabaseWrapper

    @staticmethod
    def is_in_memory_db(database_name: Union[str, PathLike]) -> bool: ...
