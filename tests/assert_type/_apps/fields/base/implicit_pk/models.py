from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class User(models.Model):
    pass


def test_add_id_field_if_no_primary_key_defined() -> None:
    # Plugin auto-injects an ``id`` AutoField when no primary key is declared.
    assert_type(User().id, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType, reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute, assert-type]  # ty: ignore[unresolved-attribute, type-assertion-failure]
