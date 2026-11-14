from __future__ import annotations

from typing import Any, assert_type

from django.db import models


class Release(models.Model):
    pk = models.CompositePrimaryKey("version", "name")
    version = models.IntegerField()
    name = models.CharField(max_length=20)


def composite_pk_reads_as_tuple(release: Release) -> None:
    assert_type(release.pk, tuple[Any, ...])  # pyright: ignore[reportAssertTypeFailure]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    release.pk = (1, "a")
    release.pk = [1, "a"]
    release.pk = None
