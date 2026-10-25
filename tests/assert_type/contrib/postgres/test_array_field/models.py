from __future__ import annotations

import uuid
from typing import Any, assert_type

from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    array = ArrayField(base_field=models.Field())


def array_field_descriptor_access() -> None:
    user = User(array=[])
    assert_type(user.array, list[Any])


class Members(models.Model):
    members = ArrayField(base_field=models.IntegerField())
    members_as_text = ArrayField(base_field=models.CharField(max_length=255))


def array_field_base_field_parsed_into_generic_typevar() -> None:
    user = Members()
    assert_type(user.members, list[int])  # pyrefly: ignore[assert-type]
    assert_type(user.members_as_text, list[str])  # pyrefly: ignore[assert-type]


class MyModel(models.Model):
    lst = ArrayField(base_field=models.CharField(max_length=100), null=True)


def nullable_array_field() -> None:
    assert_type(MyModel().lst, list[str] | None)  # pyrefly: ignore[assert-type]
    assert_type(MyModel.lst.field.base_field, models.Field[str | int, str])  # pyrefly: ignore[assert-type, missing-attribute]


class ArrayAssignments(models.Model):
    lst = ArrayField(base_field=models.CharField(max_length=100), null=False)
    null_lst = ArrayField(base_field=models.CharField(max_length=100), null=True)


def array_field_assignments_follow_column_nullability() -> None:
    instance = ArrayAssignments()
    random_uuid = uuid.uuid4()
    instance.lst = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]
    instance.lst = [random_uuid, random_uuid]  # type: ignore[list-item]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]
    instance.null_lst = None
    instance.null_lst = [random_uuid, random_uuid]  # type: ignore[list-item]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]
