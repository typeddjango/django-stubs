from django.contrib.postgres.forms.ranges import (
    DateRangeField,
    DateTimeRangeField,
    DecimalRangeField,
    IntegerRangeField,
    RangeWidget,
)
from django.forms.widgets import TextInput
from typing_extensions import assert_type

assert_type(IntegerRangeField.widget, type[TextInput] | TextInput)
assert_type(IntegerRangeField().widget, RangeWidget)

assert_type(DecimalRangeField.widget, type[TextInput] | TextInput)
assert_type(DecimalRangeField().widget, RangeWidget)

assert_type(DateTimeRangeField.widget, type[TextInput] | TextInput)
assert_type(DateTimeRangeField().widget, RangeWidget)

assert_type(DateRangeField.widget, type[TextInput] | TextInput)
assert_type(DateRangeField().widget, RangeWidget)
