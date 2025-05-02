from typing import cast

from django.contrib.postgres.forms.array import SimpleArrayField, SplitArrayField
from django.forms.fields import Field
from django.forms.widgets import Widget
from typing_extensions import assert_type

base_field = cast(Field, ...)
size = cast(int, ...)

assert_type(SimpleArrayField.widget, type[Widget] | Widget)
assert_type(SimpleArrayField(base_field).widget, Widget)

assert_type(SplitArrayField.widget, type[Widget] | Widget)
assert_type(SplitArrayField(base_field, size).widget, Widget)
