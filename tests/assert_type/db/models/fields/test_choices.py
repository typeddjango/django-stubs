from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.db import models

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


class Kind(models.TextChoices):
    A = "a", "A"


class Size(models.IntegerChoices):
    SMALL = 1, "Small"


def pairs() -> Sequence[tuple[str, str]]:
    return [("a", "A")]


def mapping() -> Mapping[str, str]:
    return {"a": "A"}


def grouped_pairs() -> Sequence[tuple[str, Sequence[tuple[str, str]]]]:
    return [("Group", pairs())]


def grouped_mapping() -> Mapping[str, Mapping[str, str]]:
    return {"Group": mapping()}


def choices_class() -> type[models.Choices]:
    return Kind


# ty drops `type[Choices]` from the union: https://github.com/astral-sh/ty/issues/4551
def field_choices() -> None:
    models.CharField(choices=Kind)  # ty: ignore[invalid-argument-type]
    models.IntegerField(choices=Size)  # ty: ignore[invalid-argument-type]
    models.CharField(choices=pairs())
    models.CharField(choices=mapping())
    models.CharField(choices=grouped_pairs())
    models.CharField(choices=grouped_mapping())
    models.CharField(choices=pairs)
    models.CharField(choices=mapping)
    models.CharField(choices=grouped_pairs)
    models.CharField(choices=grouped_mapping)
    models.CharField(choices=choices_class)
    models.CharField(choices="ab")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]


# Fields redeclaring `choices` accept the same input.
def redeclared_field_choices() -> None:
    models.GeneratedField(expression=models.Value("a"), output_field=models.CharField(), db_persist=False, choices=Kind)  # ty: ignore[invalid-argument-type]
    models.FileField(choices=Kind)  # ty: ignore[invalid-argument-type]
    models.ForeignKey("auth.User", models.CASCADE, choices=mapping())
    models.OneToOneField("auth.User", models.CASCADE, choices=mapping)
    models.ManyToManyField("auth.User", choices=Kind)  # ty: ignore[invalid-argument-type]
    ArrayField(models.CharField(), choices=Kind)  # ty: ignore[invalid-argument-type]
    PointField(choices=grouped_pairs)
