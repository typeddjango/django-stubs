from django.contrib.postgres.forms.hstore import HStoreField
from django.forms.widgets import TextInput
from typing_extensions import assert_type

assert_type(HStoreField.widget, type[TextInput] | TextInput)
assert_type(HStoreField().widget, TextInput)
