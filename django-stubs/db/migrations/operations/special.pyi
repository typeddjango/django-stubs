import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from .base import Operation

if sys.version_info < (3, 8):
    from typing_extensions import Literal, Protocol
else:
    from typing import Literal, Protocol

class SeparateDatabaseAndState(Operation):
    database_operations: Sequence[Operation] = ...
    state_operations: Sequence[Operation] = ...
    def __init__(
        self, database_operations: Sequence[Operation] = ..., state_operations: Sequence[Operation] = ...
    ) -> None: ...

class RunSQL(Operation):
    noop: Literal[""] = ...
    sql: Union[str, List[str], Tuple[str, ...]] = ...
    reverse_sql: Optional[Union[str, List[str], Tuple[str, ...]]] = ...
    state_operations: Sequence[Operation] = ...
    hints: Mapping[str, Any] = ...
    def __init__(
        self,
        sql: Union[str, List[str], Tuple[str, ...]],
        reverse_sql: Optional[Union[str, List[str], Tuple[str, ...]]] = ...,
        state_operations: Sequence[Operation] = ...,
        hints: Optional[Mapping[str, Any]] = ...,
        elidable: bool = ...,
    ) -> None: ...

class _CodeCallable(Protocol):
    def __call__(self, __state_apps: StateApps, __shema_editor: BaseDatabaseSchemaEditor) -> None: ...

class RunPython(Operation):
    code: _CodeCallable = ...
    reverse_code: Optional[_CodeCallable] = ...
    hints: Optional[Dict[str, Any]] = ...
    def __init__(
        self,
        code: _CodeCallable,
        reverse_code: Optional[_CodeCallable] = ...,
        atomic: Optional[bool] = ...,
        hints: Optional[Dict[str, Any]] = ...,
        elidable: bool = ...,
    ) -> None: ...
    @staticmethod
    def noop(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None: ...
