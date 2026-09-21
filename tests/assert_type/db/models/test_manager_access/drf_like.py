"""Plain classes hold managers too, this mirrors DRF's `GenericAPIView.queryset`."""

from __future__ import annotations

from typing import Generic, assert_type

from django.db import models
from typing_extensions import TypeVar

from .objects import Category

_MT_co = TypeVar("_MT_co", bound=models.Model, covariant=True)


class QuerySetHolder(Generic[_MT_co]):
    queryset: models.Manager[_MT_co] | models.QuerySet[_MT_co] | None = None


class CategoryHolder(QuerySetHolder[Category]):
    def assign(self) -> None:
        self.queryset = Category.objects.all()


class UnparametrizedHolder(QuerySetHolder):  # pyright: ignore[reportMissingTypeArgument]
    queryset = Category.objects


def manager_on_plain_class_is_allowed() -> None:
    assert_type(CategoryHolder().queryset, models.Manager[Category] | models.QuerySet[Category] | None)
    UnparametrizedHolder().queryset  # pyright: ignore[reportUnknownMemberType]
