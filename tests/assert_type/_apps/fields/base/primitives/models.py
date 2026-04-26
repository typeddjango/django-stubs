# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class User(models.Model):
    id = models.AutoField(primary_key=True)
    small_int = models.SmallIntegerField()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    text = models.TextField()


def test_model_fields_classes_present_as_primitives() -> None:
    user = User(small_int=1, name="user", slug="user", text="user")
    assert_type(user.id, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.small_int, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.name, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.slug, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.text, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
