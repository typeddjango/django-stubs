from collections.abc import Sequence

from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
from django.db.models.query import (
    QuerySet,
    RawQuerySet,
    aprefetch_related_objects,  # pyright: ignore[reportUnknownVariableType]
    prefetch_related_objects,  # pyright: ignore[reportUnknownVariableType]
)
from typing_extensions import assert_type

models_list: list[Model] = []
prefetch_related_objects(models_list, "pk")

models_tuple: tuple[Model, ...] = ()
prefetch_related_objects(models_tuple, "pk")

models_sequence: Sequence[Model] = []
prefetch_related_objects(models_sequence, "pk")

# failure cases
models_set: set[Model] = set()
prefetch_related_objects(models_set, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

models_frozenset: frozenset[Model] = frozenset()
prefetch_related_objects(models_frozenset, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]


async def test_async() -> None:
    await aprefetch_related_objects(models_list, "pk")
    await aprefetch_related_objects(models_tuple, "pk")
    await aprefetch_related_objects(models_sequence, "pk")

    # failure cases
    await aprefetch_related_objects(models_set, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    await aprefetch_related_objects(models_frozenset, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]


def test_in_operator(qs: QuerySet[Model], raw_qs: RawQuerySet[Model], obj: Model) -> None:
    assert_type(obj in qs, bool)
    assert_type(obj in raw_qs, bool)


def test_in_operator_with_anon(qs: QuerySet[Model], user_or_anon: Model | AnonymousUser) -> None:
    assert_type(user_or_anon in qs, bool)
