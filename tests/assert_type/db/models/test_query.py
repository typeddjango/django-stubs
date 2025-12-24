from collections.abc import Sequence

from django.db.models import Model
from django.db.models.query import (
    aprefetch_related_objects,  # pyright: ignore[reportUnknownVariableType]
    prefetch_related_objects,  # pyright: ignore[reportUnknownVariableType]
)

models_list: list[Model] = []
prefetch_related_objects(models_list, "pk")

models_tuple: tuple[Model, ...] = ()
prefetch_related_objects(models_tuple, "pk")

models_sequence: Sequence[Model] = []
prefetch_related_objects(models_sequence, "pk")

# failure cases
models_set: set[Model] = set()
prefetch_related_objects(models_set, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]

models_frozenset: frozenset[Model] = frozenset()
prefetch_related_objects(models_frozenset, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]


async def test_async() -> None:
    await aprefetch_related_objects(models_list, "pk")
    await aprefetch_related_objects(models_tuple, "pk")
    await aprefetch_related_objects(models_sequence, "pk")

    # failure cases
    await aprefetch_related_objects(models_set, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]
    await aprefetch_related_objects(models_frozenset, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]
