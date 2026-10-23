from __future__ import annotations

from decimal import Decimal
from typing import NewType, assert_type, cast

from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models.fields import CharField
from psycopg2.extras import DateTimeTZRange


class User(models.Model):
    id = models.AutoField(primary_key=True)
    small_int = models.SmallIntegerField()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    text = models.TextField()


def test_model_fields_classes_present_as_primitives() -> None:
    user = User(small_int=1, name="user", slug="user", text="user")
    assert_type(user.id, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.small_int, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.name, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.slug, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(user.text, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    time_range = pg_fields.DateTimeRangeField(null=False)
    some_decimal = models.DecimalField(max_digits=10, decimal_places=5)


def test_model_field_classes_from_existing_locations() -> None:
    booking = Booking()
    assert_type(booking.id, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(booking.time_range, DateTimeTZRange)  # pyrefly: ignore[assert-type]
    assert_type(booking.some_decimal, Decimal)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class NoPrimaryKey(models.Model):
    pass


def test_add_id_field_if_no_primary_key_defined() -> None:
    assert_type(NoPrimaryKey().id, int)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # ty: ignore[type-assertion-failure, unresolved-attribute]


class CustomPrimaryKey(models.Model):
    my_pk = models.IntegerField(primary_key=True)


def test_do_not_add_id_if_field_with_primary_key_True_defined() -> None:
    assert_type(CustomPrimaryKey().my_pk, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    CustomPrimaryKey().id  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


class MyModel(models.Model):
    nulltext = models.CharField(max_length=1, blank=True, null=True)


def blank_and_null_char_field_allows_none() -> None:
    MyModel(nulltext="")
    MyModel(nulltext=None)
    MyModel().nulltext = None
    assert_type(MyModel().nulltext, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class NotNullText(models.Model):
    notnulltext = models.CharField(max_length=1, blank=True, null=False)


def blank_and_not_null_charfield_does_not_allow_none() -> None:
    NotNullText(notnulltext=None)  # type: ignore[misc]
    NotNullText(notnulltext="")
    NotNullText().notnulltext = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]
    assert_type(NotNullText().notnulltext, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class MyUser(models.Model):
    name = models.CharField(max_length=100)


def if_field_called_on_class_return_field_itself() -> None:
    assert_type(MyUser.name.field, CharField[str | int, str])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type, missing-attribute]  # ty: ignore[type-assertion-failure]


class AuthMixin(models.Model):
    class Meta:
        abstract = True

    username = models.CharField(max_length=100)


class MixinModel(AuthMixin, models.Model):
    pass


def fields_inside_mixins_used_in_model_subclasses_resolved_as_primitives() -> None:
    assert_type(MixinModel().username, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


Year = NewType("Year", int)


class Book(models.Model):
    published = cast("models.Field[Year, Year]", models.IntegerField())


def can_narrow_field_type() -> None:
    book = Book()
    assert_type(book.published, Year)
    book.published = 2006  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-assignment]
    book.published = Year(2006)
    assert_type(book.published, Year)

    def accepts_int(arg: int) -> None: ...

    accepts_int(book.published)


class EncodedMessage(models.Model):
    message = models.BinaryField()


def test_binary_field_return_types() -> None:
    obj = EncodedMessage(message=b"\x010")
    assert_type(obj.message, bytes | memoryview[int])  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class SmallAuto(models.Model):
    small = models.SmallAutoField(primary_key=True)


def test_small_auto_field_class_presents_as_int() -> None:
    obj = SmallAuto()
    assert_type(obj.small, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]


class RenamedField(models.Model):
    modelname = models.IntegerField(name="fieldname", choices=((1, "One"),))


def test_ignores_renamed_field() -> None:
    # Ref: https://github.com/typeddjango/django-stubs/issues/1261
    # Django modifies the model so it doesn't have 'modelname', but we don't follow
    # along. But the 'name=' argument to a field isn't a documented feature.
    instance = RenamedField()
    assert_type(instance.modelname, int)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    instance.fieldname  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
    instance.modelname = 1
    instance.fieldname = 1  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
