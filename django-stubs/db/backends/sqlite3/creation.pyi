from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.sqlite3.base import DatabaseWrapper

class DatabaseCreation(BaseDatabaseCreation):
    connection: DatabaseWrapper
