from __future__ import annotations

import json
from typing import Collection
from django.forms import DateField, JSONField
from typing_extensions import assert_type

# 1. Test for BaseTemporalField (via DateField)
def test_temporal_field_input_formats() -> None:
    field = DateField(input_formats=["%Y-%m-%d"])
    assert_type(field.input_formats, Collection[str] | None)

# 2. Test for JSONField Encoder/Decoder
class MyEncoder(json.JSONEncoder):
    pass

class MyDecoder(json.JSONDecoder):
    pass

def test_json_field_serialization_types() -> None:
    field = JSONField(encoder=MyEncoder, decoder=MyDecoder)
    assert_type(field.encoder, type[json.JSONEncoder] | None)
    assert_type(field.decoder, type[json.JSONDecoder] | None)