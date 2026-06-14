from __future__ import annotations

from typing import Literal

from django.db import models
from django.db.models import IntegerField
from django.db.models.expressions import OuterRef, Subquery
from typing_extensions import assert_type


class Article(models.Model):
    pass


def direct_field_null_true_does_not_trigger_nullability_check() -> None:
    null_field = models.IntegerField(null=True)
    assert_type(null_field, IntegerField[float | int | str, int, Literal[True]])

    not_null_field = models.IntegerField(null=False)
    assert_type(not_null_field, IntegerField[float | int | str, int, Literal[False]])

    Article.objects.annotate(
        other_id=Subquery(
            Article.objects.filter(id=OuterRef("id")).values_list("id", flat=True)[:1],
            output_field=models.IntegerField(null=False),
        )
    )
