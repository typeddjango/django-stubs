from django.db.backends.base.base import BaseDatabaseWrapper


class BaseDatabaseClient:
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...