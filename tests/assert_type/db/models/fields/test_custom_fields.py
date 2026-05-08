from __future__ import annotations

from typing import Any, Generic, Literal

from django.db import models
from django.db.models.expressions import Combinable, F
from django.db.models.fields import _GT, _NT, _ST
from typing_extensions import TypeVar, assert_type

T = TypeVar("T")


class CustomFieldValue: ...


# `bool` is not assignable to upper bound `Literal[False, True]` of type variable `_NT`
# TODO: ty should reject that too
class InvalidCustomField(models.Field[_ST, _GT, bool]):  # type:ignore[type-var] # pyrefly: ignore[bad-specialization] # pyright: ignore[reportInvalidTypeArguments]
    pass


def custom_generic_field_override_typevar_defaults() -> None:
    class GenericField(models.Field[_ST, _GT, _NT]): ...

    class MyModel(models.Model):
        field = GenericField[CustomFieldValue | int, CustomFieldValue]()
        null_field = GenericField[CustomFieldValue | int, CustomFieldValue | None, Literal[True]](null=True)
        conflict_field = GenericField[CustomFieldValue | int, CustomFieldValue, Literal[False]](null=True)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
        conflict_null_field = GenericField[CustomFieldValue | int, CustomFieldValue, Literal[True]](null=False)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    instance = MyModel()
    assert_type(instance.field, CustomFieldValue)
    assert_type(instance.null_field, CustomFieldValue | None)


def single_type_field() -> None:
    class SingleTypeField(models.Field[T, T, _NT]): ...

    class MyModel(models.Model):
        field = SingleTypeField[bool]()
        explicit_null_field = SingleTypeField[bool | None, Literal[True]](null=True)
        conflict_null_field = SingleTypeField[bool](null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
        explicit_conflict_null_field = SingleTypeField[bool, Literal[False]](null=True)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    instance = MyModel()
    assert_type(instance.field, bool)
    assert_type(instance.explicit_null_field, bool | None)


def custom_explicit_get_set_field() -> None:
    class CustomValueField(models.Field[CustomFieldValue | int, CustomFieldValue, _NT]): ...

    class MyModel(models.Model):
        field = CustomValueField()
        null_field = CustomValueField(null=True)

    instance = MyModel()
    assert_type(instance.field, CustomFieldValue)
    assert_type(instance.null_field, CustomFieldValue | None)
    instance.field = CustomFieldValue()
    instance.field = 12
    instance.field = "NoNo"  # type: ignore[call-overload] # pyrefly:ignore[no-matching-overload] # ty:ignore[invalid-assignment] # pyright:ignore[reportAttributeAccessIssue]


def custom_generic_field() -> None:
    _ST_Int = TypeVar("_ST_Int", contravariant=True, default=float | int | str | Combinable)
    _GT_Int = TypeVar("_GT_Int", covariant=True, default=int)

    class CustomSmallIntegerField(models.SmallIntegerField[_ST_Int, _GT_Int, _NT]): ...

    class MyModel(models.Model):
        field = CustomSmallIntegerField()
        null_field = CustomSmallIntegerField(null=True)

    instance = MyModel()
    assert_type(instance.field, int)
    assert_type(instance.null_field, int | None)
    instance.field = 1.2
    instance.field = 12
    instance.field = "12"
    instance.field = F("id")
    instance.field = CustomFieldValue()  # type: ignore[call-overload] # pyrefly:ignore[no-matching-overload] # ty:ignore[invalid-assignment] # pyright:ignore[reportAttributeAccessIssue]


def additional_typevar_field() -> None:
    _ST_Custom = TypeVar("_ST_Custom", contravariant=True, default=CustomFieldValue | int)
    _GT_Custom = TypeVar("_GT_Custom", covariant=True, default=CustomFieldValue)

    class AdditionalTypeVarField(
        models.Field[_ST_Custom, _GT_Custom, _NT], Generic[T, _ST_Custom, _GT_Custom, _NT]
    ): ...

    class MyModel(models.Model):
        field = AdditionalTypeVarField[bool]()
        null_field = AdditionalTypeVarField[bool, CustomFieldValue | int, CustomFieldValue, Literal[True]](null=True)

    instance = MyModel()
    assert_type(instance.field, CustomFieldValue)
    assert_type(instance.null_field, CustomFieldValue | None)


def field_implicit_any() -> None:
    # This is inferred as models.Field[Any, Any, Literal[False]]
    class FieldImplicitAny(models.Field): ...

    class MyModel(models.Model):
        field = FieldImplicitAny()
        null_field = FieldImplicitAny(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    instance = MyModel()
    assert_type(instance.field, Any)
    assert_type(instance.null_field, Any)  # type:ignore[assert-type] # Mypy says `Any | None` which is a bit odd


def field_explicit_any() -> None:
    class FieldExplicitAny(models.Field[Any, Any, Any]): ...

    class MyModel(models.Model):
        field = FieldExplicitAny()
        null_field = FieldExplicitAny(null=True)

    instance = MyModel()
    assert_type(instance.field, Any)
    assert_type(instance.null_field, Any)


def field_two_typevar_form_is_still_accepted() -> None:
    class LegacyField(models.Field[CustomFieldValue | int, CustomFieldValue]): ...

    class MyModel(models.Model):
        field = LegacyField()
        null_field = LegacyField(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    instance = MyModel()
    assert_type(instance.field, CustomFieldValue)
    assert_type(instance.null_field, CustomFieldValue | None)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    instance.field = CustomFieldValue()
    instance.field = 12


def field_two_typevar_form_in_user_annotation() -> None:
    # Legacy `field: Field[A, B] = CustomField()` annotations with a legacy `CustomField` (without `_NT`)
    class CustomField(models.Field[CustomFieldValue | int, CustomFieldValue]): ...

    class MyModel(models.Model):
        field: models.Field[CustomFieldValue | int, CustomFieldValue] = CustomField()
        implicit_null_field = CustomField(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
        explicit_null_field: models.Field[CustomFieldValue | int, CustomFieldValue | None, Literal[True]] = CustomField(  # pyright: ignore[reportAssignmentType]  # pyrefly: ignore[bad-assignment]  # ty: ignore[invalid-assignment]
            null=True  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type] # ty: ignore[invalid-argument-type]
        )
        null_field: models.Field[CustomFieldValue | int, CustomFieldValue | None] = CustomField(null=True)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    instance = MyModel()
    assert_type(instance.field, CustomFieldValue)
    assert_type(instance.null_field, CustomFieldValue | None)
    assert_type(instance.implicit_null_field, CustomFieldValue | None)  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    assert_type(instance.explicit_null_field, CustomFieldValue | None)  # pyrefly: ignore[assert-type]
    instance.field = CustomFieldValue()
    instance.field = 12
    instance.field = "no"  # type: ignore[call-overload]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]  # pyright: ignore[reportAttributeAccessIssue]
    instance.null_field = None  # type: ignore[call-overload]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[invalid-assignment]  # pyright: ignore[reportAttributeAccessIssue]
    instance.null_field = CustomFieldValue()


def nullable_subclass_inherits_null_overload() -> None:
    _ST_Text = TypeVar("_ST_Text", contravariant=True, default=str | int | Combinable)
    _GT_Text = TypeVar("_GT_Text", covariant=True, default=str)
    _ST_Int = TypeVar("_ST_Int", contravariant=True, default=float | int | str | Combinable)
    _GT_Int = TypeVar("_GT_Int", covariant=True, default=int)
    _NT = TypeVar("_NT", Literal[True], Literal[False], default=Literal[False])

    class HtmlField(models.TextField[_ST_Text, _GT_Text, _NT]): ...

    class IntWrap(models.IntegerField[_ST_Int, _GT_Int, _NT]): ...

    class Article(models.Model):
        body = HtmlField()
        body_nullable = HtmlField(null=True)
        count = IntWrap()
        count_nullable = IntWrap(null=True)

    assert_type(Article().body, str)
    assert_type(Article().body_nullable, str | None)
    assert_type(Article().count, int)
    assert_type(Article().count_nullable, int | None)


def nullable_field_subclass_without_explicit_type_vars() -> None:
    """
    We auto add typevars in mypy plugin which avoid issues here.

    TODO: False positive pyrefly/ty/pyright
    """

    class HTMLField(models.TextField): ...

    class IntWrap(models.IntegerField): ...

    class FieldMixin: ...

    class MySlugField(models.SlugField, FieldMixin): ...

    class Article(models.Model):
        body = HTMLField()
        body_nullable = HTMLField(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
        count_nullable = IntWrap(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
        slug_nullable = MySlugField(null=True)  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

    assert_type(Article().body, str)
    assert_type(Article().body_nullable, str | None)  # pyrefly: ignore[assert-type] # ty: ignore[type-assertion-failure] # pyright: ignore[reportAssertTypeFailure]
    assert_type(Article().count_nullable, int | None)  # pyrefly: ignore[assert-type] # ty: ignore[type-assertion-failure] # pyright: ignore[reportAssertTypeFailure]
    assert_type(Article().slug_nullable, str | None)  # pyrefly: ignore[assert-type] # ty: ignore[type-assertion-failure] # pyright: ignore[reportAssertTypeFailure]


def test_custom_model_fields_override_init() -> None:
    """
    TODO: False positive ty/mypy
    """
    _ST_Int = TypeVar("_ST_Int", contravariant=True, default=float | int | str)
    _GT_Int = TypeVar("_GT_Int", covariant=True, default=int)
    _NT = TypeVar("_NT", Literal[True], Literal[False], default=Literal[False])

    class MyIntegerField(models.IntegerField[_ST_Int, _GT_Int, _NT]):
        def __init__(self, *args: Any, null: _NT = False, **kwargs: Any) -> None:  # type:ignore[assignment] # ty:ignore[invalid-parameter-default]
            kwargs["null"] = null
            super().__init__(*args, **kwargs)

    class User(models.Model):
        custom_int = MyIntegerField(null=False)
        custom_int_nullable = MyIntegerField(null=True)

    assert_type(User().custom_int, int)
    assert_type(User().custom_int_nullable, int | None)
