from __future__ import annotations

from typing import TYPE_CHECKING, Any, assert_type, cast

from django.contrib.postgres.fields import ArrayField
from django.db import models

if TYPE_CHECKING:
    from collections.abc import Sequence


class MyModel(models.Model):
    redefined_set_type = cast("models.Field[int, int]", models.IntegerField())
    redefined_union_set_type = cast("models.Field[int | float, int]", models.IntegerField())
    redefined_array_set_type = cast(
        "ArrayField[Sequence[int | float], int]",
        ArrayField(base_field=models.IntegerField()),
    )
    default_set_type = models.IntegerField()
    unset_set_type = cast("models.Field", models.IntegerField())
    annotated_set_type: int = models.CharField(max_length=10)  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


def field_set_type_honors_type_redefinition() -> None:
    non_init = MyModel()
    assert_type(non_init.redefined_set_type, int)
    assert_type(non_init.redefined_union_set_type, int)
    assert_type(non_init.redefined_array_set_type, list[int])  # pyrefly: ignore[assert-type]
    assert_type(non_init.default_set_type, int)
    assert_type(non_init.unset_set_type, Any)
    non_init.redefined_set_type = "invalid"  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-assignment]
    non_init.redefined_union_set_type = "invalid"  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-assignment]
    array_val: list[str] = ["invalid"]
    non_init.redefined_array_set_type = array_val  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]
    non_init.default_set_type = []  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
    non_init.unset_set_type = []
    MyModel(  # type: ignore[misc]
        redefined_set_type="invalid",
        redefined_union_set_type="invalid",
        redefined_array_set_type=33,
        default_set_type=[],
        unset_set_type=[],
        annotated_set_type="invalid",
    )
