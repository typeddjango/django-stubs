from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model

class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    connection: DatabaseWrapper
    sql_create_fk: None  # type: ignore[assignment]
    sql_alter_table_comment: None  # type: ignore[assignment]
    sql_alter_column_comment: None  # type: ignore[assignment]
    def delete_model(self, model: type[Model], handle_autom2m: bool = True) -> None: ...
