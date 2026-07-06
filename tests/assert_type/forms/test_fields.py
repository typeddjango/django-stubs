from __future__ import annotations

import json
from collections.abc import Collection
from typing import Any

from django import forms
from django.forms import DateField, JSONField
from django.forms.fields import DateTimeFormatsIterator
from typing_extensions import assert_type


# 1. Test for BaseTemporalField (via DateField)
def test_temporal_field_input_formats() -> None:
    field = DateField(input_formats=["%Y-%m-%d"])
    # Verify that 'Collection' is correctly implemented
    assert_type(field.input_formats, Collection[str] | DateTimeFormatsIterator | None)


# 2. "Real World" Example: Using it in a Django Form
class MyForm(forms.Form):
    start_date = DateField(input_formats=["%Y-%m-%d"])


def test_form_field_type_access() -> None:
    form = MyForm()
    # Fetch the field explicitly from base_fields
    field = form.base_fields["start_date"]

    # Apply type narrowing to resolve Mypy errors
    if isinstance(field, DateField):
        assert_type(field.input_formats, Collection[str] | DateTimeFormatsIterator | None)


# 3. "Real World" Example: Subclassing
class CustomDateField(DateField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(input_formats=["%d/%m/%Y"], *args, **kwargs)


def test_subclass_field_type() -> None:
    custom_field = CustomDateField()
    assert_type(custom_field.input_formats, Collection[str] | DateTimeFormatsIterator | None)


# 4. Test for JSONField Encoder/Decoder
class MyEncoder(json.JSONEncoder):
    pass


class MyDecoder(json.JSONDecoder):
    pass


def test_json_field_serialization_types() -> None:
    field = JSONField(encoder=MyEncoder, decoder=MyDecoder)
    assert_type(field.encoder, type[json.JSONEncoder] | None)
    assert_type(field.decoder, type[json.JSONDecoder] | None)
