from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from django.contrib.postgres.fields import ArrayField
from django.db import models
from typing_extensions import assert_type

if TYPE_CHECKING:
    from collections.abc import Sequence


class FieldRedefinitionModel(models.Model):
    redefined_set_type = cast("models.Field[int, int]", models.IntegerField())
    redefined_union_set_type = cast("models.Field[int | float, int]", models.IntegerField())
    redefined_array_set_type = cast(
        "ArrayField[Sequence[int | float], int]",
        ArrayField(base_field=models.IntegerField()),
    )
    default_set_type = models.IntegerField()
    unset_set_type = cast("models.Field", models.IntegerField())


def test_field_set_type_honors_type_redefinition() -> None:
    non_init = FieldRedefinitionModel()
    assert_type(non_init.redefined_set_type, int)
    assert_type(non_init.redefined_union_set_type, int)
    assert_type(non_init.redefined_array_set_type, list[int])
    assert_type(non_init.default_set_type, int)
    assert_type(non_init.unset_set_type, Any)

    non_init.redefined_set_type = "invalid"  # type: ignore[call-overload]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]
    non_init.redefined_union_set_type = "invalid"  # type: ignore[call-overload]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]
    array_val: list[str] = ["invalid"]
    non_init.redefined_array_set_type = array_val  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]
    non_init.default_set_type = []  # type: ignore[call-overload]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]
    non_init.unset_set_type = []

    FieldRedefinitionModel(  # type: ignore[misc]
        redefined_set_type="invalid",
        redefined_union_set_type="invalid",
        redefined_array_set_type=33,
        default_set_type=[],
        unset_set_type=[],
    )
