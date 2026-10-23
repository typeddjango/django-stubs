from __future__ import annotations

from typing import Any

from django.db import models

# The base resolves to `Any`, so mypy's computed MRO for the field omits the base `Field`.
_AnyBase: Any = models.DateField


class AnyBaseField(_AnyBase): ...  # type: ignore[misc]  # the Any base is the point of this repro


class LookupModel(models.Model):
    when = AnyBaseField()


def test_transform_lookup_on_any_base_field_does_not_crash() -> None:
    # Resolving a transform lookup against a field whose MRO omits `Field` must not crash the plugin.
    LookupModel.objects.filter(when__year=2020)
