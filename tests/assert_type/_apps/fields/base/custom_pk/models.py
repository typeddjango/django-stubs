# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class User(models.Model):
    my_pk = models.IntegerField(primary_key=True)


def test_do_not_add_id_if_field_with_primary_key_True_defined() -> None:
    assert_type(User().my_pk, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    # Plugin removes the auto ``id`` when an explicit primary key is defined.
    User().id  # type: ignore[attr-defined]  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
