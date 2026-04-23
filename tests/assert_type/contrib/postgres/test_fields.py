from __future__ import annotations

from typing import Any

from django.contrib.postgres.fields import DateRangeField, IntegerRangeField
from django.db import models
from typing_extensions import assert_type

# Test IntegerRangeField (checks specialized base_field)
assert_type(IntegerRangeField.base_field, type[models.IntegerField[Any, Any]])
int_field_instance = IntegerRangeField()
assert_type(int_field_instance.base_field, models.IntegerField[Any, Any])

# Test DateRangeField (ensures the Generic logic works for other types)
assert_type(DateRangeField.base_field, type[models.DateField[Any, Any]])
date_field_instance = DateRangeField()
assert_type(date_field_instance.base_field, models.DateField[Any, Any])
