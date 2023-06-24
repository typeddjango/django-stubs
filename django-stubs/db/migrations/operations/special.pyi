from collections.abc import Mapping, Sequence
from typing import Any, Literal, Protocol

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.utils.datastructures import _ListOrTuple

from .base import Operation

class SeparateDatabaseAndState(Operation):
    database_operations: Sequence[Operation]
    state_operations: Sequence[Operation]

    def __init__(
        self, database_operations: Sequence[Operation] | None = ..., state_operations: Sequence[Operation] | None = ...
    ) -> None: ...

class RunSQL(Operation):
    noop: Literal[""]
    sql: str | _ListOrTuple[str | tuple[str, dict[str, Any] | _ListOrTuple[str] | None]]
    reverse_sql: str | None | _ListOrTuple[str | tuple[str, dict[str, Any] | _ListOrTuple[str] | None]]
    state_operations: Sequence[Operation]
    hints: Mapping[str, Any]
    def __init__(
        self,
        sql: str | _ListOrTuple[str | tuple[str, dict[str, Any] | _ListOrTuple[str] | None]],
        reverse_sql: str | None | _ListOrTuple[str | tuple[str, dict[str, Any] | _ListOrTuple[str] | None]] = ...,
        state_operations: Sequence[Operation] | None = ...,
        hints: Mapping[str, Any] | None = ...,
        elidable: bool = ...,
    ) -> None: ...
    @property
    def reversible(self) -> bool: ...  # type: ignore[override]

class _CodeCallable(Protocol):
    def __call__(self, __state_apps: StateApps, __schema_editor: BaseDatabaseSchemaEditor) -> None: ...

class RunPython(Operation):
    code: _CodeCallable
    reverse_code: _CodeCallable | None
    hints: Mapping[str, Any]
    def __init__(
        self,
        code: _CodeCallable,
        reverse_code: _CodeCallable | None = ...,
        atomic: bool | None = ...,
        hints: Mapping[str, Any] | None = ...,
        elidable: bool = ...,
    ) -> None: ...
    @staticmethod
    def noop(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None: ...
    @property
    def reversible(self) -> bool: ...  # type: ignore[override]
