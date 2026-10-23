from __future__ import annotations

from typing import Any, Generic, assert_type

from django.db import models
from django.db.models import fields
from typing_extensions import TypeVar

_ST = TypeVar("_ST", contravariant=True)
_GT = TypeVar("_GT", covariant=True)

T = TypeVar("T")


class CustomFieldValue: ...


class GenericField(fields.Field[_ST, _GT]): ...


class SingleTypeField(fields.Field[T, T]): ...


class CustomValueField(fields.Field[CustomFieldValue | int, CustomFieldValue]): ...


class AdditionalTypeVarField(fields.Field[_ST, _GT], Generic[_ST, _GT, T]): ...


class CustomSmallIntegerField(fields.SmallIntegerField[_ST, _GT]): ...


class FieldImplicitAny(fields.Field): ...


class FieldExplicitAny(fields.Field[Any, Any]): ...


class User(models.Model):
    id = models.AutoField(primary_key=True)
    my_custom_field1 = GenericField[CustomFieldValue | int, CustomFieldValue]()
    my_custom_field2 = CustomValueField()
    my_custom_field3 = SingleTypeField[bool]()
    my_custom_field4 = AdditionalTypeVarField[CustomFieldValue | int, CustomFieldValue, bool]()
    my_custom_field_any1 = FieldImplicitAny()
    my_custom_field_any2 = FieldExplicitAny()

    # test null=True on fields with non-optional generic types throw error
    my_custom_field5 = GenericField[CustomFieldValue | int, CustomFieldValue](null=True)  # type: ignore[misc]
    my_custom_field6 = CustomValueField(null=True)  # type: ignore[misc]
    my_custom_field7 = SingleTypeField[bool](null=True)  # type: ignore[misc]
    my_custom_field8 = AdditionalTypeVarField[CustomFieldValue | int, CustomFieldValue, bool](null=True)  # type: ignore[misc]
    my_custom_field9 = fields.Field[CustomFieldValue | int, CustomFieldValue](null=True)  # type: ignore[misc]

    # test overriding fields that set _pyi_private_set_type or _pyi_private_get_type
    my_custom_field10 = fields.SmallIntegerField[bool, bool]()
    my_custom_field11 = CustomSmallIntegerField[bool, bool]()

    # test null=True on fields with non-optional generic types throw no errors
    my_custom_field12 = fields.Field[CustomFieldValue | int, CustomFieldValue | None](null=True)
    my_custom_field13 = GenericField[CustomFieldValue | int, CustomFieldValue | None](null=True)
    my_custom_field14 = SingleTypeField[bool | None](null=True)
    my_custom_field15 = fields.Field[None, None](null=True)

    # test null=True on Any does not raise
    my_custom_field_any3 = FieldImplicitAny(null=True)
    my_custom_field_any4 = FieldExplicitAny(null=True)


def test_custom_model_fields_with_generic_type() -> None:
    user = User()
    assert_type(user.id, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field1, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field2, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field3, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field4, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field5, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field6, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field7, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field8, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field9, CustomFieldValue)
    assert_type(user.my_custom_field10, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field11, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field12, CustomFieldValue | None)
    assert_type(user.my_custom_field13, CustomFieldValue | None)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field14, bool | None)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field15, None)

    assert_type(user.my_custom_field_any1, Any)
    assert_type(user.my_custom_field_any2, Any)
    assert_type(user.my_custom_field_any3, Any | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field_any4, Any)  # pyrefly: ignore[assert-type]


TextFieldAlias = models.TextField
BoolFieldAlias = models.Field[bool, bool]


class AliasedTextField(TextFieldAlias): ...


class AliasedBoolField(BoolFieldAlias): ...


class AliasUser(models.Model):
    text = AliasedTextField()
    nullable_text = AliasedTextField(null=True)
    flag = AliasedBoolField()


def test_custom_field_subclassing_an_alias() -> None:
    user = AliasUser()
    assert_type(user.text, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.nullable_text, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.flag, bool)  # pyrefly: ignore[assert-type]
