from typing import Any

from django.db.models.sql.compiler import _AsSqlType

class SpatialOperator:
    sql_template: Any
    op: Any
    func: Any
    def __init__(self, op: Any | None = ..., func: Any | None = ...) -> None: ...
    @property
    def default_template(self) -> Any: ...
    def as_sql(self, connection: Any, lookup: Any, template_params: Any, sql_params: Any) -> _AsSqlType: ...
