from __future__ import annotations

from typing import assert_type

from django.db.models import BinaryField
from django.db.models.fields import CharField
from django.db.models.functions import Left, Right, Substr


def func_resolve_output_field() -> None:
    def expect_func_binary(func: Substr[BinaryField] | Left[BinaryField] | Right[BinaryField]) -> None:
        return None

    bin_sub = Substr("username", 1, 100, output_field=BinaryField())
    str_sub = Substr("username", 1, 100)  # Default to `CharField` per `Substr.output_field`

    bin_left = Left("username", 5, output_field=BinaryField())
    str_left = Left("username", 5)  # Default to `CharField` per `Left.output_field`

    bin_right = Right("username", 5, output_field=BinaryField())
    str_right = Right("username", 5)  # Default to `CharField` per `Right.output_field`

    assert_type(str_sub, Substr[CharField])
    assert_type(str_left, Left[CharField])
    assert_type(str_right, Right[CharField])

    expect_func_binary(bin_sub)
    expect_func_binary(str_sub)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    expect_func_binary(bin_left)
    expect_func_binary(str_left)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    expect_func_binary(bin_right)
    expect_func_binary(str_right)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
