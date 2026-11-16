from __future__ import annotations

from typing import assert_type

from django.contrib.postgres.fields import CICharField, CIEmailField, CITextField
from django.db import models


class CIModel(models.Model):
    char = CICharField(max_length=10)
    null_char = CICharField(max_length=10, null=True)
    email = CIEmailField()
    null_email = CIEmailField(null=True)
    text = CITextField()
    null_text = CITextField(null=True)


def citext_fields_follow_column_nullability() -> None:
    instance = CIModel()
    assert_type(instance.char, str)
    assert_type(instance.null_char, str | None)
    assert_type(instance.email, str)
    assert_type(instance.null_email, str | None)
    assert_type(instance.text, str)
    assert_type(instance.null_text, str | None)
