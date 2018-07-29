from django.db.backends.base.base import BaseDatabaseWrapper


class BaseDatabaseFeatures:
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...