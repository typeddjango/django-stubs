from __future__ import annotations

from collections.abc import Callable
from typing import assert_type

from django.db import connection, connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorWrapper

with connection.cursor() as cursor:
    assert_type(cursor, CursorWrapper)
    cursor.execute("SELECT %s", [123])

# psycopg2 composable SQL
from psycopg2.sql import SQL, Identifier

with connection.cursor() as cursor:
    cursor.execute(SQL("INSERT INTO {} VALUES (%s)").format(Identifier("my_table")), [123])

assert_type(connections["test"], BaseDatabaseWrapper)
for conn in connections.all():
    with conn.cursor() as cursor:
        assert_type(cursor, CursorWrapper)

for sids, func, robust in connection.run_on_commit:
    assert_type(sids, set[str])
    assert_type(func, Callable[[], object])
    assert_type(robust, bool)
