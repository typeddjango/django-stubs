from __future__ import annotations

import datetime
import decimal
import uuid
from decimal import Decimal
from typing import Any, NewType, assert_type, cast

from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.db.models.fields import CharField
from psycopg2.extras import DateTimeTZRange


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    time_range = pg_fields.DateTimeRangeField(null=False)
    some_decimal = models.DecimalField(max_digits=10, decimal_places=5)


def test_model_field_classes_from_existing_locations() -> None:
    booking = Booking()
    assert_type(booking.id, int)
    assert_type(booking.time_range, DateTimeTZRange)
    assert_type(booking.some_decimal, Decimal)


class NoPrimaryKey(models.Model):
    pass


def test_add_id_field_if_no_primary_key_defined() -> None:
    assert_type(NoPrimaryKey().id, int)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # ty: ignore[type-assertion-failure, unresolved-attribute]  # pyrefly: ignore[assert-type, missing-attribute]


class CustomPrimaryKey(models.Model):
    my_pk = models.IntegerField(primary_key=True)


def test_do_not_add_id_if_field_with_primary_key_True_defined() -> None:
    assert_type(CustomPrimaryKey().my_pk, int)
    CustomPrimaryKey().id  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


class MyModel(models.Model):
    nulltext = models.CharField(max_length=1, blank=True, null=True)


def blank_and_null_char_field_allows_none() -> None:
    MyModel(nulltext="")
    MyModel(nulltext=None)
    MyModel().nulltext = None
    assert_type(MyModel().nulltext, str | None)


class NotNullText(models.Model):
    notnulltext = models.CharField(max_length=1, blank=True, null=False)


def blank_and_not_null_charfield_does_not_allow_none() -> None:
    NotNullText(notnulltext=None)  # type: ignore[misc]
    NotNullText(notnulltext="")
    NotNullText().notnulltext = None  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]
    assert_type(NotNullText().notnulltext, str)


class MyUser(models.Model):
    name = models.CharField(max_length=100)


def if_field_called_on_class_return_field_itself() -> None:
    assert_type(MyUser.name.field, CharField[str | int, str])


class AuthMixin(models.Model):
    class Meta:
        abstract = True

    username = models.CharField(max_length=100)


class MixinModel(AuthMixin, models.Model):
    pass


def fields_inside_mixins_used_in_model_subclasses_resolved_as_primitives() -> None:
    assert_type(MixinModel().username, str)


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
    assert_type(obj.message, bytes | memoryview[int])


class SmallAuto(models.Model):
    small = models.SmallAutoField(primary_key=True)


def test_small_auto_field_class_presents_as_int() -> None:
    obj = SmallAuto()
    assert_type(obj.small, int)


class RenamedField(models.Model):
    modelname = models.IntegerField(name="fieldname", choices=((1, "One"),))


def test_ignores_renamed_field() -> None:
    # Ref: https://github.com/typeddjango/django-stubs/issues/1261
    # Django modifies the model so it doesn't have 'modelname', but we don't follow
    # along. But the 'name=' argument to a field isn't a documented feature.
    instance = RenamedField()
    assert_type(instance.modelname, int)
    instance.fieldname  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
    instance.modelname = 1
    instance.fieldname = 1  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]


class AllFields(models.Model):
    id = models.AutoField(primary_key=True)

    # Integer-family
    integer = models.IntegerField()
    small_int = models.SmallIntegerField()
    big_int = models.BigIntegerField()
    pos_int = models.PositiveIntegerField()
    pos_small_int = models.PositiveSmallIntegerField()
    pos_big_int = models.PositiveBigIntegerField()
    null_integer = models.IntegerField(null=True)
    null_small_int = models.SmallIntegerField(null=True)
    null_big_int = models.BigIntegerField(null=True)
    null_pos_int = models.PositiveIntegerField(null=True)
    null_pos_small_int = models.PositiveSmallIntegerField(null=True)
    null_pos_big_int = models.PositiveBigIntegerField(null=True)

    # Float / Decimal
    flt = models.FloatField()
    null_flt = models.FloatField(null=True)
    dec = models.DecimalField(max_digits=10, decimal_places=5)
    null_dec = models.DecimalField(max_digits=10, decimal_places=5, null=True)

    # Char-family
    name = models.CharField(max_length=255)
    null_name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255)
    null_slug = models.SlugField(max_length=255, null=True)
    text = models.TextField()
    null_text = models.TextField(null=True)
    csv_int = models.CommaSeparatedIntegerField(max_length=255)
    null_csv_int = models.CommaSeparatedIntegerField(max_length=255, null=True)
    email = models.EmailField()
    null_email = models.EmailField(null=True)
    url = models.URLField()
    null_url = models.URLField(null=True)

    # Boolean
    flag = models.BooleanField()
    null_flag = models.BooleanField(null=True)

    # IP addresses
    ip = models.IPAddressField()
    null_ip = models.IPAddressField(null=True)
    gen_ip = models.GenericIPAddressField()
    null_gen_ip = models.GenericIPAddressField(null=True)

    # Date / time / duration
    day = models.DateField()
    null_day = models.DateField(null=True)
    moment = models.DateTimeField()
    null_moment = models.DateTimeField(null=True)
    clock = models.TimeField()
    null_clock = models.TimeField(null=True)
    duration = models.DurationField()
    null_duration = models.DurationField(null=True)

    # UUID
    uid = models.UUIDField()
    null_uid = models.UUIDField(null=True)

    # Binary
    blob = models.BinaryField()
    null_blob = models.BinaryField(null=True)

    # JSON / FilePath
    payload = models.JSONField()
    null_payload = models.JSONField(null=True)
    payload_with_db_default = models.JSONField(default=dict, db_default={})
    path = models.FilePathField()
    null_path = models.FilePathField(null=True)


def every_builtin_field_reads_null_true_as_optional() -> None:
    instance = AllFields()
    assert_type(instance.id, int)

    assert_type(instance.integer, int)
    assert_type(instance.null_integer, int | None)
    assert_type(instance.small_int, int)
    assert_type(instance.null_small_int, int | None)
    assert_type(instance.big_int, int)
    assert_type(instance.null_big_int, int | None)
    assert_type(instance.pos_int, int)
    assert_type(instance.null_pos_int, int | None)
    assert_type(instance.pos_small_int, int)
    assert_type(instance.null_pos_small_int, int | None)
    assert_type(instance.pos_big_int, int)
    assert_type(instance.null_pos_big_int, int | None)

    assert_type(instance.flt, float)
    assert_type(instance.null_flt, float | None)
    assert_type(instance.dec, decimal.Decimal)
    assert_type(instance.null_dec, decimal.Decimal | None)

    assert_type(instance.name, str)
    assert_type(instance.null_name, str | None)
    assert_type(instance.slug, str)
    assert_type(instance.null_slug, str | None)
    assert_type(instance.text, str)
    assert_type(instance.null_text, str | None)
    assert_type(instance.csv_int, str)
    assert_type(instance.null_csv_int, str | None)
    assert_type(instance.email, str)
    assert_type(instance.null_email, str | None)
    assert_type(instance.url, str)
    assert_type(instance.null_url, str | None)

    assert_type(instance.flag, bool)
    assert_type(instance.null_flag, bool | None)

    assert_type(instance.ip, str)
    assert_type(instance.null_ip, str | None)
    assert_type(instance.gen_ip, str)
    assert_type(instance.null_gen_ip, str | None)

    assert_type(instance.day, datetime.date)
    assert_type(instance.null_day, datetime.date | None)
    assert_type(instance.moment, datetime.datetime)
    assert_type(instance.null_moment, datetime.datetime | None)
    assert_type(instance.clock, datetime.time)
    assert_type(instance.null_clock, datetime.time | None)
    assert_type(instance.duration, datetime.timedelta)
    assert_type(instance.null_duration, datetime.timedelta | None)

    assert_type(instance.uid, uuid.UUID)
    assert_type(instance.null_uid, uuid.UUID | None)

    assert_type(instance.blob, bytes | memoryview[int])
    assert_type(instance.null_blob, bytes | memoryview[int] | None)

    assert_type(instance.payload, Any)
    assert_type(instance.null_payload, Any | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(instance.payload_with_db_default, Any)
    assert_type(instance.path, Any)
    assert_type(instance.null_path, Any | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]


def if_field_called_on_class_keeps_null_in_its_type() -> None:
    assert_type(AllFields.null_name.field, CharField[str | int | None, str | None])
