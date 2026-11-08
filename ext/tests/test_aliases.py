from __future__ import annotations

from typing import Any, TypedDict

from django.db.models import Model

from django_stubs_ext import ValuesQuerySet, WithAnnotations


def test_extends_values_queryset() -> None:
    class MyQS(ValuesQuerySet[Any, Any]):
        pass


def test_with_annotations_accepts_two_params() -> None:
    class Extra(TypedDict):
        foo: str

    WithAnnotations[Model, Extra]
