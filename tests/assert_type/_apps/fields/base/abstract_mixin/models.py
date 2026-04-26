# pyright: reportUnknownVariableType=none
from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class AuthMixin(models.Model):
    class Meta:
        abstract = True

    username = models.CharField(max_length=100)


class MyModel(AuthMixin, models.Model):
    pass


def fields_inside_mixins_used_in_model_subclasses_resolved_as_primitives() -> None:
    assert_type(MyModel().username, str)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
