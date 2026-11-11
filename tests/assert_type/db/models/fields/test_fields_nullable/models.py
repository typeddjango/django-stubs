from __future__ import annotations

import datetime
import decimal
from typing import assert_type

from django.db import models
from django.db.models import IntegerField, OuterRef, Subquery
from typing_extensions import TypeVar

_ST_contra = TypeVar("_ST_contra", contravariant=True)
_GT_co = TypeVar("_GT_co", covariant=True)


class MyModel(models.Model):
    text_nullable = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=100)


def nullable_field_with_strict_optional_true() -> None:
    assert_type(MyModel().text, str)
    assert_type(MyModel().text_nullable, str | None)
    MyModel().text = None  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]
    MyModel().text_nullable = None


def nullable() -> bool:
    return True


class NullFromBool(models.Model):
    text = models.CharField(max_length=100, null=nullable())  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]  # ty: ignore[deprecated]  # pyrefly: ignore[deprecated]


class BlankNotNull(models.Model):
    notnulltext = models.CharField(max_length=1, blank=True, null=False)


def blank_and_not_null_charfield_does_not_allow_none() -> None:
    BlankNotNull(notnulltext=None)  # type: ignore[misc]


class HtmlField(models.TextField[_ST_contra, _GT_co]): ...


class IntWrap(models.IntegerField[_ST_contra, _GT_co]): ...


class Article(models.Model):
    body = HtmlField()  # pyright: ignore[reportUnknownVariableType]
    body_nullable = HtmlField(null=True)  # pyright: ignore[reportUnknownVariableType]
    count = IntWrap()  # pyright: ignore[reportUnknownVariableType]
    count_nullable = IntWrap(null=True)  # pyright: ignore[reportUnknownVariableType]


def nullable_subclass_inherits_null_overload() -> None:
    # The type vars have no defaults, so only the plugin resolves a bare call, from the nearest base's defaults.
    # pyrefly and ty still solve `null=True` from the inherited self-annotated overload,
    # pyright doesn't: https://github.com/microsoft/pyright/issues/11989
    assert_type(Article().body, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(Article().body_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]
    assert_type(Article().count, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(Article().count_nullable, int | None)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]


class SubqueryArticle(models.Model):
    pass


def direct_field_null_true_does_not_trigger_nullability_check() -> None:
    field = models.IntegerField(null=True)
    assert_type(field, IntegerField[float | int | str | None, int | None])
    not_null_field = models.IntegerField(null=False)
    assert_type(not_null_field, IntegerField[float | int | str, int])
    SubqueryArticle.objects.annotate(
        other_id=Subquery(
            SubqueryArticle.objects.filter(id=OuterRef("id")).values_list("id", flat=True)[:1],
            output_field=models.IntegerField(null=True),
        )
    )


def field_null_true_expression_does_not_trigger_nullability_check() -> None:
    def take_field(f: models.Field) -> None:
        return None

    take_field(models.IntegerField(null=True))
    take_field(models.IntegerField(null=False))


class HTMLField(models.TextField): ...


class BareIntWrap(models.IntegerField): ...


class FieldMixin: ...


class MySlugField(models.SlugField, FieldMixin): ...


class BareArticle(models.Model):
    body = HTMLField()
    body_nullable = HTMLField(null=True)
    count_nullable = BareIntWrap(null=True)
    slug_nullable = MySlugField(null=True)


def nullable_field_subclass_without_explicit_type_vars() -> None:
    assert_type(BareArticle().body, str)
    # A bare subclass is pinned to its parent's non-null defaults, only the plugin can widen it
    assert_type(BareArticle().body_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(BareArticle().count_nullable, int | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(BareArticle().slug_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]


class MixedIntegerField(FieldMixin, models.IntegerField[_ST_contra, _GT_co]): ...


# The type vars have no defaults, so only the plugin resolves them, walking past the mixin.
class MixinFirstArticle(models.Model):
    count = MixedIntegerField()  # pyright: ignore[reportUnknownVariableType]
    count_nullable = MixedIntegerField(null=True)  # pyright: ignore[reportUnknownVariableType]


def generic_subclass_with_mixin_before_the_field_resolves_the_defaults() -> None:
    assert_type(MixinFirstArticle().count, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]  # pyrefly: ignore[assert-type]
    assert_type(MixinFirstArticle().count_nullable, int | None)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]


class PositionalArgs(models.Model):
    amount = models.DecimalField(None, None, 10, 2, null=True)  # max_digits/decimal_places positional
    day = models.DateField(None, None, False, False, null=True)  # auto_now/auto_now_add positional
    moment = models.TimeField(None, None, False, False, null=True)
    stamp = models.DateTimeField(None, None, False, False, null=True)
    addr = models.GenericIPAddressField(None, None, "both", False, null=True)  # protocol/unpack_ipv4


def positional_overload_args_with_null_true_select_nullable_overload() -> None:
    instance = PositionalArgs()
    assert_type(instance.amount, decimal.Decimal | None)
    assert_type(instance.day, datetime.date | None)
    assert_type(instance.moment, datetime.time | None)
    assert_type(instance.stamp, datetime.datetime | None)
    assert_type(instance.addr, str | None)
