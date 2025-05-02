from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.forms.widgets import Widget
from typing_extensions import assert_type

assert_type(ReadOnlyPasswordHashField.widget, type[Widget] | Widget)
assert_type(ReadOnlyPasswordHashField().widget, Widget)

assert_type(UsernameField.widget, type[Widget] | Widget)
assert_type(UsernameField().widget, Widget)
