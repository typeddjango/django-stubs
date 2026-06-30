from __future__ import annotations

from django.db import connection, connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorWrapper
from typing_extensions import assert_type

with connection.cursor() as cursor:
    assert_type(cursor, CursorWrapper)
    cursor.execute("SELECT %s", [123])

# psycopg2 composable SQL
from psycopg2.sql import SQL, Identifier  # type: ignore[import-untyped]

with connection.cursor() as cursor:
    cursor.execute(SQL("INSERT INTO {} VALUES (%s)").format(Identifier("my_table")), [123])

assert_type(connections["test"], BaseDatabaseWrapper)
for conn in connections.all():
    with conn.cursor() as cursor:
        assert_type(cursor, CursorWrapper)
