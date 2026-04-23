from __future__ import annotations

from django.contrib.postgres.fields import DateRangeField, IntegerRangeField
from django.db import models
from typing_extensions import assert_type

# Test IntegerRangeField (checks specialized base_field)
assert_type(IntegerRangeField.base_field, type[models.IntegerField])
int_field_instance = IntegerRangeField()
assert_type(int_field_instance.base_field, models.IntegerField)

# Test DateRangeField (ensures the Generic logic works for other types)
assert_type(DateRangeField.base_field, type[models.DateField])
date_field_instance = DateRangeField()
assert_type(date_field_instance.base_field, models.DateField)
