"""Regression test for https://github.com/typeddjango/django-stubs/issues/2911.

A TypeVar with a forward-referenced bound used in a QuerySet subclass
caused 'Must not defer during final iteration' crash in mypy.
"""

from __future__ import annotations

from django.db import models
from django.db.models.query import QuerySet
from typing_extensions import TypeVar

T = TypeVar("T", bound="MyModel")


class MyModelQuerySet(QuerySet[T]):
    pass


class MyModel(models.Model):
    class Meta:
        app_label = "myapp"
