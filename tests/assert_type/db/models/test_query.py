from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from django.contrib.auth.models import Group, Permission
from django.db.models import Model, Prefetch
from django.db.models.query import QuerySet, RawQuerySet, aprefetch_related_objects, prefetch_related_objects

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.contrib.auth.models import AnonymousUser

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


def test_in_operator(
    qs: QuerySet[Model],
    raw_qs: RawQuerySet[Model],
    obj: Model,
    user_or_anon: Model | AnonymousUser,
    obj_or_none: Model | None,
) -> None:
    assert_type(obj in qs, bool)
    assert_type(obj in raw_qs, bool)
    assert_type(user_or_anon in qs, bool)
    assert_type(obj_or_none in qs, bool)
    assert_type(None in qs, bool)
    assert_type("test" in qs, bool)
    assert_type(42 in qs, bool)


def test_class_getitem_returns_the_class(qs_class: type[QuerySet[Model]]) -> None:
    assert_type(qs_class.__class_getitem__(Model), type[QuerySet[Model]])


def prefetch_related_keeps_the_queryset_type(groups: QuerySet[Group], perms: QuerySet[Permission]) -> None:
    prefetch = Prefetch("permissions", queryset=perms)
    assert_type(prefetch.queryset, QuerySet[Permission] | None)
    assert_type(groups.prefetch_related(prefetch), QuerySet[Group])
    assert_type(perms.prefetch_related("content_type"), QuerySet[Permission])
    assert_type(groups.prefetch_related(None), QuerySet[Group])
    assert_type(Group.objects.prefetch_related(prefetch), QuerySet[Group])
    groups.prefetch_related(1)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue, reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
    # `None` clears the lookups, so it can't be mixed with other lookups
    groups.prefetch_related(None, "permissions")  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
