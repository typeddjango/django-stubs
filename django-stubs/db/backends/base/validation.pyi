from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.fields import Field
from typing import (
    Any,
    List,
)


class BaseDatabaseValidation:
    def __init__(self, connection: BaseDatabaseWrapper) -> None: ...
    def check_field(self, field: Field, **kwargs) -> List[Any]: ...