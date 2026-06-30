from __future__ import annotations

from django.contrib.auth.hashers import check_password
from typing_extensions import assert_type


def setter(password: str | None) -> None: ...


def bad_setter(password: int) -> None: ...


assert_type(check_password("password", "encoded"), bool)
assert_type(check_password("password", "encoded", setter), bool)
check_password("password", "encoded", bad_setter)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
