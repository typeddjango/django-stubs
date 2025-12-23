from collections.abc import Sequence

from django.db.models import Model
from django.db.models.query import prefetch_related_objects

models_list: list[Model] = []
prefetch_related_objects(models_list, "pk")

models_tuple: tuple[Model, ...] = ()
prefetch_related_objects(models_tuple, "pk")

models_sequence: Sequence[Model] = []
prefetch_related_objects(models_sequence, "pk")

# failure cases
models_set: set[Model] = set()
prefetch_related_objects(models_set, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

models_frozenset: frozenset[Model] = frozenset()
prefetch_related_objects(models_frozenset, "pk")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
