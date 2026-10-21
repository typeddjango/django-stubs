from __future__ import annotations

import datetime
from collections.abc import Iterator
from typing import Any, assert_type

from django.db import models
from django.db.models.query import QuerySet, RawQuerySet
from django.utils import timezone


class Blog(models.Model):
    created_at = models.DateTimeField()


def queryset_methods_keep_the_row_type(qs: QuerySet[Blog], manager: models.Manager[Blog]) -> None:
    assert_type(qs.get(id=1), Blog)
    assert_type(iter(qs), Iterator[Blog])
    assert_type(qs.iterator(), Iterator[Blog])
    assert_type(qs.first(), Blog | None)
    assert_type(qs.earliest(), Blog)
    assert_type(qs[0], Blog)
    assert_type(qs[:9], QuerySet[Blog, Blog])
    assert_type(qs.create(), Blog)
    assert_type(qs.get_or_create(), tuple[Blog, bool])
    assert_type(qs.exists(), bool)
    assert_type(qs.none(), QuerySet[Blog, Blog])
    assert_type(qs.update_or_create(), tuple[Blog, bool])
    assert_type(qs.explain(), str)
    assert_type(qs.raw(qs.explain()), RawQuerySet[Blog])
    assert_type(qs.distinct(), QuerySet[Blog, Blog])
    assert_type(qs.distinct("created_at"), QuerySet[Blog, Blog])
    assert_type(qs & qs, QuerySet[Blog, Blog])
    # .dates / .datetimes swap the row type
    assert_type(manager.dates("created_at", "day"), QuerySet[Blog, datetime.date])
    assert_type(manager.datetimes("created_at", "day"), QuerySet[Blog, datetime.datetime])
    # defer / only
    assert_type(qs.defer("created_at"), QuerySet[Blog, Blog])
    assert_type(qs.defer(None), QuerySet[Blog, Blog])
    assert_type(qs.only("created_at"), QuerySet[Blog, Blog])
    qs.only(None)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    # bulk methods
    assert_type(qs.count(), int)
    assert_type(qs.update(created_at=timezone.now()), int)
    assert_type(qs.in_bulk(), dict[Any, Blog])
    assert_type(qs.bulk_update(list(qs), fields=["created_at"]), int)
    assert_type(qs.bulk_create([]), list[Blog])
    assert_type(qs.delete(), tuple[int, dict[str, int]])
