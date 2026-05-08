from __future__ import annotations

import datetime
import decimal
import uuid
from typing import Any, Literal, NewType, cast

from django.db import models
from django.db.models import CharField
from django.db.models.fields import IntegerField, _FieldDescriptor
from typing_extensions import assert_type


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
assert_type(instance.null_payload, Any | None)
assert_type(instance.payload_with_db_default, Any)
assert_type(instance.path, Any)
assert_type(instance.null_path, Any | None)


def if_field_called_on_class_return_field_itself() -> None:
    assert_type(
        AllFields.name.field,
        CharField[str | int, str, Literal[False]],
    )
    assert_type(
        AllFields.null_name.field,
        CharField[str | int, str, Literal[True]],
    )


def null_char_field_allows_none() -> None:
    AllFields(null_name="")
    AllFields(null_name=None)
    AllFields().null_name = None


def not_null_charfield_does_not_allow_none() -> None:
    AllFields(name="")
    AllFields(name=None)
    AllFields().name = None  # type: ignore[call-overload] # pyrefly:ignore[no-matching-overload] # ty:ignore[invalid-assignment] # pyright:ignore[reportAttributeAccessIssue]


def fields_on_non_model_classes_resolve_to_field_type() -> None:
    class MyClass:
        myfield = models.IntegerField[int, int]()

    assert_type(MyClass.myfield, _FieldDescriptor[IntegerField[int, int, Literal[False]]])
    assert_type(MyClass.myfield.field, IntegerField[int, int, Literal[False]])
    assert_type(MyClass().myfield, IntegerField[int, int, Literal[False]])


def fields_inside_mixins_used_in_model_subclasses_resolved_as_primitives() -> None:
    class AuthMixin(models.Model):
        class Meta:
            abstract = True

        username = models.CharField(max_length=100)
        null_username = models.CharField(max_length=100, null=True)

    class MyModel(AuthMixin, models.Model):
        pass

    assert_type(MyModel().username, str)
    assert_type(MyModel().null_username, str | None)


def test_small_auto_field_class_presents_as_int() -> None:
    class MyModel(models.Model):
        small = models.SmallAutoField(primary_key=True)

    obj = MyModel()

    assert_type(obj.small, int)


def can_narrow_field_type() -> None:
    Year = NewType("Year", int)

    class Book(models.Model):
        published = cast("models.Field[Year, Year]", models.IntegerField())

    book = Book()
    assert_type(book.published, Year)
    book.published = (  # type: ignore[call-overload] # pyrefly:ignore[no-matching-overload] # ty:ignore[invalid-assignment] # pyright:ignore[reportAttributeAccessIssue]
        2006
    )
    book.published = Year(2006)
    assert_type(book.published, Year)  # N: Revealed type is "main.Year"

    def accepts_int(arg: int) -> None: ...

    accepts_int(book.published)


def test_ignores_renamed_field() -> None:
    """
    Ref: https://github.com/typeddjango/django-stubs/issues/1261
    Django modifies the model so it doesn't have 'modelname', but we don't follow
    along. But the 'name=' argument to a field isn't a documented feature.
    """

    class RenamedField(models.Model):
        modelname = models.IntegerField(name="fieldname", choices=((1, "One"),))

    instance = RenamedField()
    assert_type(instance.modelname, int)
    instance.fieldname  # type: ignore[attr-defined] # pyrefly:ignore[missing-attribute] # ty:ignore[unresolved-attribute] # pyright:ignore[reportAttributeAccessIssue,reportUnknownMemberType]
    instance.modelname = 1
    instance.fieldname = 1  # type: ignore[attr-defined] # pyrefly:ignore[missing-attribute] # ty:ignore[unresolved-attribute] # pyright:ignore[reportAttributeAccessIssue]


def nullable_field_with_strict_optional_true() -> None:
    class MyModel(models.Model):
        text_nullable = models.CharField(max_length=100, null=True)
        text = models.CharField(max_length=100)

    MyModel().text = None  # type: ignore[call-overload] # pyrefly:ignore[no-matching-overload] # ty:ignore[invalid-assignment] # pyright:ignore[reportAttributeAccessIssue]
    MyModel().text_nullable = None
