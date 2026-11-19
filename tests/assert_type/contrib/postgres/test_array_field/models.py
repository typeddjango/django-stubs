from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Literal, assert_type, overload

from django.contrib.postgres.fields import ArrayField
from django.db import models
from typing_extensions import TypeVar, Unpack, deprecated

if TYPE_CHECKING:
    from django.db.models.fields import FieldInitKwargs


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
    assert_type(user.members, list[int])
    assert_type(user.members_as_text, list[str])


class MyModel(models.Model):
    lst = ArrayField(base_field=models.CharField(max_length=100), null=True)


def nullable_array_field() -> None:
    assert_type(MyModel().lst, list[str] | None)
    assert_type(MyModel.lst.field, ArrayField[Sequence[str | int] | None, list[str] | None])


class ArrayAssignments(models.Model):
    lst = ArrayField(base_field=models.CharField(max_length=100), null=False)
    null_lst = ArrayField(base_field=models.CharField(max_length=100), null=True)


def array_field_assignments_follow_column_nullability() -> None:
    instance = ArrayAssignments()
    random_uuid = uuid.uuid4()
    instance.lst = None  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]
    instance.lst = [random_uuid, random_uuid]  # type: ignore[list-item]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]
    instance.null_lst = None
    instance.null_lst = [random_uuid, random_uuid]  # type: ignore[list-item]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]


# Subclasses, as documented in the README
_ST_contra = TypeVar("_ST_contra", contravariant=True, default=Sequence[Any])
_GT_co = TypeVar("_GT_co", covariant=True, default=list[Any])
_ElemST = TypeVar("_ElemST")
_ElemGT = TypeVar("_ElemGT")


class SetArrayField(ArrayField[set[Any], set[Any]]): ...


class BareArrayField(ArrayField): ...


class DefaultsArrayField(ArrayField[_ST_contra, _GT_co]): ...


class MyArrayField(ArrayField[_ST_contra, _GT_co]):
    @overload
    def __init__(
        self: MyArrayField[Sequence[_ElemST], list[_ElemGT]],
        base_field: models.Field[_ElemST, _ElemGT],
        size: int | None = None,
        *,
        verbose_name: str | None = None,
        name: str | None = None,
        null: Literal[False] = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self: MyArrayField[Sequence[_ElemST] | None, list[_ElemGT] | None],
        base_field: models.Field[_ElemST, _ElemGT],
        size: int | None = None,
        *,
        verbose_name: str | None = None,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        base_field: models.Field[Any, Any],
        size: int | None = None,
        *,
        verbose_name: str | None = None,
        name: str | None = None,
        null: Literal[False] = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        base_field: models.Field[Any, Any],
        size: int | None = None,
        *,
        verbose_name: str | None = None,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    @deprecated("`null` must be a literal `True` or `False` for the field type to be inferred")
    def __init__(
        self,
        base_field: models.Field[Any, Any],
        size: int | None = None,
        *,
        verbose_name: str | None = None,
        name: str | None = None,
        null: bool,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class MyArraySubField(MyArrayField): ...


class ArraySubclasses(models.Model):
    as_set = SetArrayField(models.IntegerField())
    # a subclass without type parameters stays off the deprecated overload
    null_bare = BareArrayField(models.IntegerField(), null=True)
    defaults = DefaultsArrayField(models.IntegerField())
    null_defaults = DefaultsArrayField(models.IntegerField(), null=True)
    overloaded = MyArrayField(models.IntegerField())
    null_overloaded = MyArrayField(models.IntegerField(), null=True)


def array_field_subclasses(flag: bool) -> None:
    instance = ArraySubclasses()
    assert_type(instance.as_set, set[Any])
    # mypy and pyright read `list[Any]`, they don't solve a subclass's type parameters from inherited overloads:
    # https://github.com/python/mypy/issues/22395 and https://github.com/microsoft/pyright/issues/11989
    assert_type(instance.defaults, list[int])  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]
    assert_type(instance.null_defaults, list[int] | None)  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]
    MyArrayField(models.IntegerField(), null=flag)  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # pyrefly: ignore[deprecated]  # ty: ignore[deprecated]
    # a subclass without type parameters stays off the deprecated overload
    MyArraySubField(models.IntegerField(), null=True)
    assert_type(instance.overloaded, list[int])
    assert_type(instance.null_overloaded, list[int] | None)
