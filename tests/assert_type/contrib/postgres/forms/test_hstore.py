from django.contrib.postgres.forms.hstore import HStoreField
from django.forms.widgets import Widget
from typing_extensions import assert_type

assert_type(HStoreField.widget, type[Widget] | Widget)
assert_type(HStoreField().widget, Widget)
