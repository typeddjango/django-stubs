from django.contrib.postgres.forms.ranges import (
    DateRangeField,
    DateTimeRangeField,
    DecimalRangeField,
    IntegerRangeField,
)
from django.forms.widgets import Widget
from typing_extensions import assert_type

assert_type(IntegerRangeField.widget, type[Widget] | Widget)
assert_type(IntegerRangeField().widget, Widget)

assert_type(DecimalRangeField.widget, type[Widget] | Widget)
assert_type(DecimalRangeField().widget, Widget)

assert_type(DateTimeRangeField.widget, type[Widget] | Widget)
assert_type(DateTimeRangeField().widget, Widget)

assert_type(DateRangeField.widget, type[Widget] | Widget)
assert_type(DateRangeField().widget, Widget)
