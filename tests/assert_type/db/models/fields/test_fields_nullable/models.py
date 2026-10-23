from __future__ import annotations

from typing import assert_type

from django.db import models
from django.db.models import IntegerField, OuterRef, Subquery
from typing_extensions import TypeVar

_ST = TypeVar("_ST", contravariant=True)
_GT = TypeVar("_GT", covariant=True)


class MyModel(models.Model):
    text_nullable = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=100)


def nullable_field_with_strict_optional_true() -> None:
    assert_type(MyModel().text, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(MyModel().text_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    MyModel().text = None  # type: ignore[assignment]  # pyrefly: ignore[bad-assignment]
    MyModel().text_nullable = None


class HtmlField(models.TextField[_ST, _GT]): ...


class IntWrap(models.IntegerField[_ST, _GT]): ...


class Article(models.Model):
    body = HtmlField()  # pyright: ignore[reportUnknownVariableType]
    body_nullable = HtmlField(null=True)  # pyright: ignore[reportUnknownVariableType]
    count = IntWrap()  # pyright: ignore[reportUnknownVariableType]
    count_nullable = IntWrap(null=True)  # pyright: ignore[reportUnknownVariableType]


def nullable_subclass_inherits_null_overload() -> None:
    assert_type(Article().body, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]
    assert_type(Article().body_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]
    assert_type(Article().count, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]
    assert_type(Article().count_nullable, int | None)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # ty: ignore[type-assertion-failure]


class SubqueryArticle(models.Model):
    pass


def direct_field_null_true_does_not_trigger_nullability_check() -> None:
    field = models.IntegerField(null=True)
    assert_type(field, IntegerField[float | int | str | None, int | None])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
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


class BareArticle(models.Model):
    body = HTMLField()
    body_nullable = HTMLField(null=True)
    count_nullable = BareIntWrap(null=True)


def nullable_field_subclass_without_explicit_type_vars() -> None:
    assert_type(BareArticle().body, str)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(BareArticle().body_nullable, str | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
    assert_type(BareArticle().count_nullable, int | None)  # pyright: ignore[reportAssertTypeFailure]  # ty: ignore[type-assertion-failure]
