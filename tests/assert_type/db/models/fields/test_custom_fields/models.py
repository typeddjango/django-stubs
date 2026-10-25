from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Literal, assert_type, overload

from django.db import models
from django.db.models import fields
from django.db.models.expressions import F
from typing_extensions import TypeVar, Unpack

if TYPE_CHECKING:
    from django.db.models.fields import FieldInitKwargs

_ST = TypeVar("_ST", contravariant=True)
_GT = TypeVar("_GT", covariant=True)

T = TypeVar("T")


class CustomFieldValue: ...


class GenericField(fields.Field[_ST, _GT]): ...


class SingleTypeField(fields.Field[T, T]): ...


class CustomValueField(fields.Field[CustomFieldValue | int, CustomFieldValue]): ...


class AdditionalTypeVarField(fields.Field[_ST, _GT], Generic[_ST, _GT, T]): ...


# Generic type arguments


class CustomSmallIntegerField(fields.SmallIntegerField[_ST, _GT]): ...


class User(models.Model):
    id = models.AutoField(primary_key=True)
    my_custom_field1 = GenericField[CustomFieldValue | int, CustomFieldValue]()
    my_custom_field2 = CustomValueField()
    my_custom_field3 = SingleTypeField[bool]()
    my_custom_field4 = AdditionalTypeVarField[CustomFieldValue | int, CustomFieldValue, bool]()

    # test overriding fields that set _pyi_private_set_type or _pyi_private_get_type
    my_custom_field10 = fields.SmallIntegerField[bool, bool]()
    my_custom_field11 = CustomSmallIntegerField[bool, bool]()


def test_custom_model_fields_with_generic_type() -> None:
    user = User()
    assert_type(user.id, int)
    assert_type(user.my_custom_field1, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field2, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field3, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field4, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field10, bool)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field11, bool)  # pyrefly: ignore[assert-type]


def custom_value_field_set_type() -> None:
    user = User()
    user.my_custom_field2 = CustomFieldValue()
    user.my_custom_field2 = 12
    user.my_custom_field2 = "NoNo"  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]


class TwoTypeVarAnnotation(models.Model):
    field: models.Field[CustomFieldValue | int, CustomFieldValue] = CustomValueField()


def field_two_typevar_form_in_user_annotation() -> None:
    instance = TwoTypeVarAnnotation()
    assert_type(instance.field, CustomFieldValue)
    instance.field = CustomFieldValue()
    instance.field = 12
    instance.field = "no"  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-assignment]


# null=True on generic type arguments


class NullableUser(models.Model):
    # test null=True on fields with non-optional generic types throw error
    my_custom_field5 = GenericField[CustomFieldValue | int, CustomFieldValue](null=True)
    my_custom_field6 = CustomValueField(null=True)  # type: ignore[misc]
    my_custom_field7 = SingleTypeField[bool](null=True)  # type: ignore[misc]
    my_custom_field8 = AdditionalTypeVarField[CustomFieldValue | int, CustomFieldValue, bool](null=True)  # type: ignore[misc]
    my_custom_field9 = fields.Field[CustomFieldValue | int, CustomFieldValue](null=True)

    # test null=True on fields with optional generic types throw no errors
    my_custom_field12 = fields.Field[CustomFieldValue | int, CustomFieldValue | None](null=True)
    my_custom_field13 = GenericField[CustomFieldValue | int, CustomFieldValue | None](null=True)
    my_custom_field14 = SingleTypeField[bool | None](null=True)
    my_custom_field15 = fields.Field[None, None](null=True)


def custom_fields_with_null_true() -> None:
    user = NullableUser()
    assert_type(user.my_custom_field5, CustomFieldValue | None)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field6, CustomFieldValue | None)  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field7, bool | None)  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field8, CustomFieldValue | None)  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field9, CustomFieldValue | None)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field12, CustomFieldValue | None)
    assert_type(user.my_custom_field13, CustomFieldValue | None)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field14, bool | None)  # pyrefly: ignore[assert-type]
    assert_type(user.my_custom_field15, None)


class ConcreteField(fields.Field[str, str]): ...


class AlreadyOptionalField(fields.Field[str | None, str | None]): ...


class ConcreteNull(models.Model):
    ok = ConcreteField()
    # A fully-bound field can't fold `| None` into a concrete get type, so the plugin flags it.
    # Widen the get type instead.
    bad = ConcreteField(null=True)  # type: ignore[misc]
    already_optional = AlreadyOptionalField(null=True)


def concrete_custom_field_null_requires_optional_get_type() -> None:
    instance = ConcreteNull()
    assert_type(instance.ok, str)  # pyrefly: ignore[assert-type]
    assert_type(instance.bad, str | None)  # type: ignore[assert-type]  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(instance.already_optional, str | None)  # pyrefly: ignore[assert-type]


# Any type arguments


class FieldImplicitAny(fields.Field): ...


class FieldExplicitAny(fields.Field[Any, Any]): ...


class AnyUser(models.Model):
    my_custom_field_any1 = FieldImplicitAny()
    my_custom_field_any2 = FieldExplicitAny()

    # test null=True on Any does not raise
    my_custom_field_any3 = FieldImplicitAny(null=True)
    my_custom_field_any4 = FieldExplicitAny(null=True)


def custom_fields_with_any_type_args() -> None:
    user = AnyUser()
    assert_type(user.my_custom_field_any1, Any)
    assert_type(user.my_custom_field_any2, Any)
    assert_type(user.my_custom_field_any3, Any | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.my_custom_field_any4, Any)  # pyrefly: ignore[assert-type]


# Aliased base fields


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
    assert_type(user.text, str)
    assert_type(user.nullable_text, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.flag, bool)  # pyrefly: ignore[assert-type]


# Generic subclasses default their type vars like the parent field, so bare calls resolve without the plugin
_ST_Int = TypeVar("_ST_Int", contravariant=True, default=float | int | str)
_GT_Int = TypeVar("_GT_Int", covariant=True, default=int)
_ST_Custom = TypeVar("_ST_Custom", contravariant=True, default=CustomFieldValue | int)
_GT_Custom = TypeVar("_GT_Custom", covariant=True, default=CustomFieldValue)
_ST_Text = TypeVar("_ST_Text", contravariant=True, default=str)
_GT_Text = TypeVar("_GT_Text", covariant=True, default=str)


class DefaultedSmallIntegerField(fields.SmallIntegerField[_ST_Int, _GT_Int]): ...


class DefaultedAdditionalTypeVarField(fields.Field[_ST_Custom, _GT_Custom], Generic[T, _ST_Custom, _GT_Custom]): ...


class DefaultedHtmlField(models.TextField[_ST_Text, _GT_Text]): ...


class DefaultedTypeVars(models.Model):
    small_int = DefaultedSmallIntegerField()
    null_small_int = DefaultedSmallIntegerField(null=True)
    additional = DefaultedAdditionalTypeVarField[bool]()
    null_additional = DefaultedAdditionalTypeVarField[bool, CustomFieldValue | int | None, CustomFieldValue | None]()
    html = DefaultedHtmlField()
    # The cross-checker recipe for a nullable custom field: widen the generic parameters with `| None`
    null_html = DefaultedHtmlField[str | None, str | None]()


def custom_fields_with_defaulted_type_vars() -> None:
    instance = DefaultedTypeVars()
    assert_type(instance.small_int, int)
    assert_type(instance.null_small_int, int | None)  # pyright: ignore[reportAssertTypeFailure]
    assert_type(instance.additional, CustomFieldValue)  # pyrefly: ignore[assert-type]
    assert_type(instance.null_additional, CustomFieldValue | None)  # pyrefly: ignore[assert-type]
    assert_type(instance.html, str)
    assert_type(instance.null_html, str | None)  # pyrefly: ignore[assert-type]
    instance.small_int = 1.2  # pyrefly: ignore[bad-assignment]
    instance.small_int = 12
    instance.small_int = "12"  # pyrefly: ignore[bad-assignment]
    instance.small_int = F("id")  # pyrefly: ignore[bad-assignment]
    instance.small_int = CustomFieldValue()  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]


# Constructor overloads, as documented in the README


class MyIntegerField(models.IntegerField[_ST_Int, _GT_Int]):
    @overload
    def __init__(
        self: MyIntegerField[float | int | str | None, int | None],
        verbose_name: str | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self,
        verbose_name: str | None = None,
        name: str | None = None,
        *,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class OverloadedInit(models.Model):
    custom_int = MyIntegerField(null=False)
    custom_int_nullable = MyIntegerField(null=True)


def custom_model_field_override_init_via_overloads() -> None:
    # a bad kwarg is rejected through the Unpack'd TypedDict, on every checker
    MyIntegerField(nul=True)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
    assert_type(OverloadedInit().custom_int, int)
    assert_type(OverloadedInit().custom_int_nullable, int | None)
