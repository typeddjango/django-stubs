from collections.abc import Sequence
from enum import Enum
from typing import Any, TypeVar, overload

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models.base import Model
from django.db.models.expressions import Combinable
from django.db.models.query_utils import Q

_T = TypeVar("_T", bound="BaseConstraint")

class Deferrable(Enum):
    DEFERRED: str
    IMMEDIATE: str

class BaseConstraint:
    name: str
    def __init__(self, name: str) -> None: ...
    def constraint_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def create_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def remove_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def deconstruct(self) -> Any: ...
    def clone(self: _T) -> _T: ...

class CheckConstraint(BaseConstraint):
    check: Q
    def __init__(self, *, check: Q, name: str) -> None: ...

class UniqueConstraint(BaseConstraint):
    expressions: tuple[Combinable, ...]
    fields: tuple[str, ...]
    condition: Q | None
    deferrable: Deferrable | None

    @overload
    def __init__(
        self,
        *expressions: str | Combinable,
        fields: None = ...,
        name: str,
        condition: Q | None = ...,
        deferrable: Deferrable | None = ...,
        include: Sequence[str] | None = ...,
        opclasses: Sequence[Any] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        fields: Sequence[str],
        name: str,
        condition: Q | None = ...,
        deferrable: Deferrable | None = ...,
        include: Sequence[str] | None = ...,
        opclasses: Sequence[Any] = ...,
    ) -> None: ...
