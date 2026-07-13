from __future__ import annotations

from typing import Literal

from django.db.models import BinaryField
from django.db.models.fields import CharField
from django.db.models.functions import Left, Right, Substr
from typing_extensions import assert_type


def func_resolve_output_field() -> None:
    def expect_func_binary(func: Substr[BinaryField] | Left[BinaryField] | Right[BinaryField]) -> None:
        return None

    bin_sub = Substr("username", 1, 100, output_field=BinaryField())
    str_sub = Substr("username", 1, 100)  # Default to `CharField` per `Substr.output_field`

    bin_left = Left("username", 5, output_field=BinaryField())
    str_left = Left("username", 5)  # Default to `CharField` per `Left.output_field`

    bin_right = Right("username", 5, output_field=BinaryField())
    str_right = Right("username", 5)  # Default to `CharField` per `Right.output_field`

    assert_type(  # False positive -> # ty: ignore[type-assertion-failure]
        bin_sub,
        Substr[BinaryField[bytes | bytearray | memoryview[int], bytes | memoryview[int], Literal[False]]],
    )
    assert_type(str_sub, Substr[CharField[str | int, str, Literal[False]]])

    assert_type(  # False positive -> # ty: ignore[type-assertion-failure]
        bin_left,
        Left[BinaryField[bytes | bytearray | memoryview[int], bytes | memoryview[int], Literal[False]]],
    )
    assert_type(str_left, Left[CharField[str | int, str, Literal[False]]])

    assert_type(  # False positive -> # ty: ignore[type-assertion-failure]
        bin_right,
        Right[BinaryField[bytes | bytearray | memoryview[int], bytes | memoryview[int], Literal[False]]],
    )
    assert_type(str_right, Right[CharField[str | int, str, Literal[False]]])

    expect_func_binary(bin_sub)  # False positive -> # ty: ignore[invalid-argument-type]
    expect_func_binary(str_sub)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    expect_func_binary(bin_left)  # False positive -> # ty: ignore[invalid-argument-type]
    expect_func_binary(str_left)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    expect_func_binary(bin_right)  # False positive -> # ty: ignore[invalid-argument-type]
    expect_func_binary(str_right)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
