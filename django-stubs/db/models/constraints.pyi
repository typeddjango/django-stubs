from collections.abc import Sequence
from enum import Enum
from typing import Any, overload

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models.base import Model
from django.db.models.expressions import BaseExpression, Combinable
from django.db.models.query_utils import Q
from django.utils.functional import _StrOrPromise
from typing_extensions import Self

class Deferrable(Enum):
    DEFERRED: str
    IMMEDIATE: str

class BaseConstraint:
    name: str
    violation_error_message: _StrOrPromise | None
    default_violation_error_message: _StrOrPromise
    def __init__(self, name: str, violation_error_message: _StrOrPromise | None = ...) -> None: ...
    def constraint_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def create_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def remove_sql(self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None) -> str: ...
    def deconstruct(self) -> tuple[str, Sequence[Any], dict[str, Any]]: ...
    def clone(self) -> Self: ...

class CheckConstraint(BaseConstraint):
    check: Q | BaseExpression
    def __init__(
        self, *, check: Q | BaseExpression, name: str, violation_error_message: _StrOrPromise | None = ...
    ) -> None: ...

class UniqueConstraint(BaseConstraint):
    expressions: Sequence[BaseExpression | Combinable]
    fields: Sequence[str]
    condition: Q | None
    deferrable: Deferrable | None

    @overload
    def __init__(
        self,
        *expressions: str | BaseExpression | Combinable,
        fields: None = ...,
        name: str,
        condition: Q | None = ...,
        deferrable: Deferrable | None = ...,
        include: Sequence[str] | None = ...,
        opclasses: Sequence[Any] = ...,
        violation_error_message: _StrOrPromise | None = ...,
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
        violation_error_message: _StrOrPromise | None = ...,
    ) -> None: ...
