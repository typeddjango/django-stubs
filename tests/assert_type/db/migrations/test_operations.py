from django.db.migrations import RunSQL

RunSQL(sql="SOME SQL")

RunSQL(sql=("SOME SQLS", "SOME SQLS"), reverse_sql=("SOME SQLS", "SOME SQLS"))

RunSQL(sql=["SOME SQLS", "SOME SQLS"], reverse_sql=["SOME SQLS", "SOME SQLS"])

RunSQL(
    sql=["SOME SQLS", ("SOME SQLS %s", ("SQL PARAM AS A TUPLE",))],
    reverse_sql=["SOME SQLS", ("SOME SQLS %s", ("SQL PARAM AS A TUPLE",))],
)

RunSQL(
    sql=["SOME SQLS", ("SOME SQLS NO PARAM", None)],
    reverse_sql=["SOME SQLS", ("SOME SQLS NO PARAM", None)],
)

RunSQL(
    sql=["SOME SQLS", ("SOME SQLS %(VAL)s", {"VAL": "FOO"})],
    reverse_sql=["SOME SQLS", ("SOME SQLS %(VAL)s", {"VAL": "FOO"})],
)

RunSQL(
    sql=["SOME SQLS", ("SOME SQLS %s, %s", ["PARAM", "ANOTHER PARAM"])],
    reverse_sql=["SOME SQLS", ("SOME SQLS %s, %s", ["PARAM", "ANOTHER PARAM"])],
)

RunSQL("INSERT INTO musician (name) VALUES ('Reinhardt');")
RunSQL([("INSERT INTO musician (name) VALUES ('Reinhardt');", None)])
RunSQL([("INSERT INTO musician (name) VALUES (%s);", ["Reinhardt"])])

query = "UPDATE posts SET category = %s WHERE category = ANY(%s);"
RunSQL([(query, ["new category", ["retired category", "another retired category"]])])

RunSQL(sql=["SOME SQLS", ("SOME SQLS %s, %s", [object(), "ANOTHER PARAM"])])

# Error cases
RunSQL(sql=("SOME SQL", {}))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
RunSQL(sql=("SOME SQL", 1))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
RunSQL(sql=("SOME SQL", None))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
RunSQL(sql=("SOME SQLS %(VAL)s", {1: "FOO"}))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
