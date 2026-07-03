from __future__ import annotations

from typing import Literal

from django.db.models import AutoField, CharField, IntegerField

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


# --- `_NT` is invariant ---
# Nullable and non-nullable fields are not interchangeable in either direction.
not_null: IntegerField[int, int, Literal[False]] = IntegerField()
nullable: IntegerField[int, int, Literal[True]] = IntegerField(null=True)
bad_to_nullable: IntegerField[int, int, Literal[True]] = not_null  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
bad_to_non_nullable: IntegerField[int, int, Literal[False]] = nullable  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


# --- Variance with non-default TypeVar bounds ---
# CharField specializes the bounds (`_ST=str | int`, `_GT=str`); the same variance rules still apply.

# ST contravariance: source set-type wider than target → OK.
char_wide_set: CharField[str | int, str] = CharField()
char_narrow_set: CharField[str, str] = char_wide_set

# GT covariance: source get-type narrower than target → OK.
char_narrow_get: CharField[str, str] = CharField[str, str]()
char_wide_get: CharField[str, str | bytes] = char_narrow_get

# ST narrowing in source → forbidden.
char_narrow: CharField[str, str] = CharField[str, str]()
char_rejected_st: CharField[str | int, str] = char_narrow  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]

# GT widening in source → forbidden.
char_wide: CharField[str, str | bytes] = CharField[str, str | bytes]()
char_rejected_gt: CharField[str, str] = char_wide  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


# --- Subclass relationships respect ST/GT variance ---
# A more concrete `Field` subtype is assignable to its base `Field` so long as ST/GT are compatible.
auto: AutoField[int, int] = AutoField[int, int]()
as_int: IntegerField[int, int] = auto

# The reverse — base to derived — is not allowed.
as_auto: AutoField[int, int] = IntegerField[int, int]()  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
