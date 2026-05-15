from __future__ import annotations

from typing import Any

from django.db import models


def field_null_true_expression_does_not_trigger_nullability_check() -> None:
    """
    Field[Any, Any, Any] as function type arg should accept both nullable and non-nullable fields
    """

    def take_field(f: models.Field[Any, Any, Any]) -> None:
        return None

    take_field(models.IntegerField(null=True))
    take_field(models.IntegerField(null=False))
