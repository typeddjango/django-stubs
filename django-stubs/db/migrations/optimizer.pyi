from typing import List

from django.db.migrations.operations.base import Operation

class MigrationOptimizer:
    def optimize(self, operations: List[Operation], app_label: str | None) -> List[Operation]: ...
    def optimize_inner(self, operations: List[Operation], app_label: str | None) -> List[Operation]: ...
