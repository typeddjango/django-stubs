from __future__ import annotations

from typing import Any, assert_type

from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    array = ArrayField(base_field=models.Field())


def array_field_descriptor_access() -> None:
    user = User(array=[])
    assert_type(user.array, list[Any])  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class Members(models.Model):
    members = ArrayField(base_field=models.IntegerField())
    members_as_text = ArrayField(base_field=models.CharField(max_length=255))


def array_field_base_field_parsed_into_generic_typevar() -> None:
    user = Members()
    assert_type(user.members, list[int])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.members_as_text, list[str])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]


class MyModel(models.Model):
    lst = ArrayField(base_field=models.CharField(max_length=100), null=True)


def nullable_array_field() -> None:
    assert_type(MyModel().lst, list[str] | None)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
