from typing import Any

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Expression
from django.utils.datastructures import DictWrapper

class GeneratedField(models.Field):
    def __init__(
        self, *, expression: Expression, output_field: models.Field, db_persist: bool | None = ..., **kwargs: Any
    ): ...
    def generated_sql(self, connection: BaseDatabaseWrapper) -> tuple[str, Any]: ...
    def db_type_parameters(self, connection: BaseDatabaseWrapper) -> DictWrapper: ...
