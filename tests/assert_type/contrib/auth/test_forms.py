from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UsernameField
from django.forms.widgets import TextInput
from typing_extensions import assert_type

assert_type(
    ReadOnlyPasswordHashField.widget,
    type[ReadOnlyPasswordHashWidget] | ReadOnlyPasswordHashWidget,
)
assert_type(ReadOnlyPasswordHashField().widget, ReadOnlyPasswordHashWidget)

assert_type(UsernameField.widget, type[TextInput] | TextInput)
assert_type(UsernameField().widget, TextInput)
