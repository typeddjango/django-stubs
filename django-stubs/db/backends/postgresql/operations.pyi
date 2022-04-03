from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.postgresql.base import DatabaseWrapper

class DatabaseOperations(BaseDatabaseOperations):
    connection: DatabaseWrapper
