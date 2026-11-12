from __future__ import annotations

from collections.abc import Callable
from typing import Any, assert_type

from django.contrib.auth.models import Permission
from django.core.management.color import no_style
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
assert_type(connection.ops.sequence_reset_sql(no_style(), [Permission]), list[str])
for conn in connections.all():
    with conn.cursor() as cursor:
        assert_type(cursor, CursorWrapper)

for sids, func, robust in connection.run_on_commit:
    assert_type(sids, set[str])
    assert_type(func, Callable[[], object])
    assert_type(robust, bool)


def blocker(
    execute: Callable[[str, Any, bool, dict[str, Any]], Any], sql: str, params: Any, many: bool, context: dict[str, Any]
) -> Any:
    return execute(sql, params, many, context)


with connection.execute_wrapper(blocker) as entered:
    assert_type(entered, None)
with connection.constraint_checks_disabled() as disabled:
    assert_type(disabled, None)
