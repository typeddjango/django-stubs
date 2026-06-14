from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class User(models.Model):
    pass


def test_add_id_field_if_no_primary_key_defined() -> None:
    assert_type(User().id, int)  # pyrefly:ignore[missing-attribute, assert-type] # ty:ignore[type-assertion-failure, unresolved-attribute] # pyright:ignore[reportAttributeAccessIssue,reportUnknownMemberType, reportAssertTypeFailure]
