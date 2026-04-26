# pyright: reportUnknownVariableType=none
"""Ref: https://github.com/typeddjango/django-stubs/issues/1261

Plugin doesn't follow the (undocumented) ``name=`` argument.
"""

from __future__ import annotations

from django.db import models
from typing_extensions import assert_type


class RenamedField(models.Model):
    modelname = models.IntegerField(name="fieldname", choices=((1, "One"),))


def test_ignores_renamed_field() -> None:
    instance = RenamedField()
    assert_type(instance.modelname, int)  # pyright: ignore[reportAssertTypeFailure, reportUnknownMemberType]  # pyrefly: ignore[assert-type]  # ty: ignore[type-assertion-failure]
    instance.fieldname  # type: ignore[attr-defined]  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
    instance.modelname = 1
    instance.fieldname = 1  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]  # pyrefly: ignore[missing-attribute]  # ty: ignore[unresolved-attribute]
