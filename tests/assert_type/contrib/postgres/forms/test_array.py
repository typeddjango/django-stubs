from typing import cast

from django.contrib.postgres.forms.array import SimpleArrayField, SplitArrayField, SplitArrayWidget
from django.forms.fields import Field
from django.forms.widgets import TextInput
from typing_extensions import assert_type

base_field = cast(Field, ...)
size = cast(int, ...)

assert_type(SimpleArrayField.widget, type[TextInput] | TextInput)
assert_type(SimpleArrayField(base_field).widget, TextInput)

assert_type(SplitArrayField.widget, type[TextInput] | TextInput)
assert_type(SplitArrayField(base_field, size).widget, SplitArrayWidget)
