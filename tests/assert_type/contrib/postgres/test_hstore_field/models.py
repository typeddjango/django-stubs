from __future__ import annotations

from typing import assert_type

from django.contrib.postgres.fields import HStoreField
from django.db import models


class Store(models.Model):
    data = HStoreField()
    null_data = HStoreField(null=True)


def hstore_field_reads_str_dict() -> None:
    store = Store()
    assert_type(store.data, dict[str, str | None])
    assert_type(store.null_data, dict[str, str | None] | None)
    values: dict[str, str] = {"a": "b"}
    store.data = values
    store.data = None  # type: ignore[assignment]  # pyright: ignore[reportAttributeAccessIssue]  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-argument-type]
