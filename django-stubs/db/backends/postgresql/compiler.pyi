from typing import Any

from django.db.models.sql.compiler import SQLAggregateCompiler as SQLAggregateCompiler
from django.db.models.sql.compiler import SQLCompiler as BaseSQLCompiler
from django.db.models.sql.compiler import SQLDeleteCompiler as SQLDeleteCompiler
from django.db.models.sql.compiler import SQLInsertCompiler as BaseSQLInsertCompiler
from django.db.models.sql.compiler import SQLUpdateCompiler as SQLUpdateCompiler

__all__ = [
    "SQLAggregateCompiler",
    "SQLCompiler",
    "SQLDeleteCompiler",
    "SQLInsertCompiler",
    "SQLUpdateCompiler",
]

class InsertUnnest(list[str]): ...

class SQLCompiler(BaseSQLCompiler):
    def quote_name_unless_alias(self, name: str) -> str: ...

class SQLInsertCompiler(BaseSQLInsertCompiler):
    def assemble_as_sql(self, fields: Any, value_rows: Any) -> tuple[Any, Any]: ...
