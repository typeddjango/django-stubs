from __future__ import annotations

from django.db.models import AutoField, IntegerField

# --- `_ST` is contravariant ---
# A field whose set-type is wider can stand in for one whose set-type is narrower.
wide_set: AutoField[int | str, int] = AutoField()
narrow_set: AutoField[int, int] = wide_set

# Reverse direction is rejected: a narrower set-type cannot stand in for a wider one.
narrow_set2: AutoField[int, int] = AutoField[int, int]()
rejected_set: AutoField[int | str, int] = narrow_set2  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


# --- `_GT` is covariant ---
# A field whose get-type is narrower can stand in for one whose get-type is wider.
narrow_get: AutoField[int, int] = AutoField[int, int]()
wide_get: AutoField[int, int | str] = narrow_get

# Reverse direction is rejected: a wider get-type cannot stand in for a narrower one.
wide_get2: AutoField[int, int | str] = AutoField[int, int | str]()
rejected_get: AutoField[int, int] = wide_get2  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


# --- Subclass relationships respect ST/GT variance ---
# A more concrete `Field` subtype is assignable to its base `Field` so long as ST/GT are compatible.
auto: AutoField[int, int] = AutoField[int, int]()
as_int: IntegerField[int, int] = auto

# The reverse — base to derived — is not allowed.
as_auto: AutoField[int, int] = IntegerField[int, int]()  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
