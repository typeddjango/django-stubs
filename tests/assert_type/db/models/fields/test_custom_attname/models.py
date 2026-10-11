from __future__ import annotations

from typing import assert_type

from django.db import models
from typing_extensions import override


class CompressedTextField(models.BinaryField[str, str]):
    @override
    def get_attname(self) -> str:
        return f"{self.name}_zlib"


class Article(models.Model):
    body = CompressedTextField()


def init_accepts_name_and_custom_attname() -> None:
    article = Article(body="hello")
    assert_type(article.body, str)
    assert_type(article.body_zlib, str)  # pyright: ignore[reportAssertTypeFailure, reportAttributeAccessIssue, reportUnknownMemberType]  # pyrefly: ignore[assert-type, missing-attribute]  # ty: ignore[type-assertion-failure, missing-attribute]
    Article(body_zlib="hello")
    Article(body=b"hello")  # type: ignore[misc]


def create_accepts_name_and_custom_attname() -> None:
    Article.objects.create(body="hello")
    Article.objects.create(body_zlib="hello")


def filter_accepts_name_and_custom_attname() -> None:
    Article.objects.filter(body="hello")
    Article.objects.filter(body_zlib="hello")


def get_or_create_accepts_name_and_custom_attname() -> None:
    Article.objects.get_or_create(body_zlib="hello", defaults={"body": "hello"})
    Article.objects.get_or_create(body="hello", defaults={"body_zlib": "hello"})
