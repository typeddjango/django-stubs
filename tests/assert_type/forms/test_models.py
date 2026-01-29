from __future__ import annotations

from typing import Any

from django import forms
from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=100)


def callback_optional(db_field: models.Field[Any, Any], **kwargs: Any) -> forms.Field | None:
    return db_field.formfield(**kwargs)


def callback_required(db_field: models.Field[Any, Any], **kwargs: Any) -> forms.Field:
    return forms.CharField()


forms.fields_for_model(MyModel, formfield_callback=callback_optional)
forms.fields_for_model(MyModel, formfield_callback=callback_required)
