from typing import (
    Any,
    Optional,
)


class MigrationOptimizer:
    def optimize(self, operations: Any, app_label: Optional[str] = ...) -> Any: ...
    def optimize_inner(self, operations: Any, app_label: Optional[str] = ...) -> Any: ...