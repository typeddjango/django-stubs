from typing import Any

from django import forms
from django.db.models.fields import _ErrorMessagesT
from django.forms.widgets import MultiWidget, _OptAttrs
from psycopg2.extras import Range

class RangeWidget(MultiWidget):
    def __init__(self, base_widget: forms.Widget | type[forms.Widget], attrs: _OptAttrs | None = ...) -> None: ...
    def decompress(self, value: Any) -> tuple[Any | None, Any | None]: ...

class HiddenRangeWidget(RangeWidget):
    def __init__(self, attrs: _OptAttrs | None = ...) -> None: ...

class BaseRangeField(forms.MultiValueField):
    default_error_messages: _ErrorMessagesT
    base_field: type[forms.Field]
    range_type: type[Range]
    hidden_widget: type[forms.Widget]
    def __init__(self, **kwargs: Any) -> None: ...
    def prepare_value(self, value: Any) -> Any: ...
    def compress(self, values: tuple[Any | None, Any | None]) -> Range | None: ...

class IntegerRangeField(BaseRangeField):
    default_error_messages: _ErrorMessagesT
    base_field: type[forms.Field]
    range_type: type[Range]

class DecimalRangeField(BaseRangeField):
    default_error_messages: _ErrorMessagesT
    base_field: type[forms.Field]
    range_type: type[Range]

class DateTimeRangeField(BaseRangeField):
    default_error_messages: _ErrorMessagesT
    base_field: type[forms.Field]
    range_type: type[Range]

class DateRangeField(BaseRangeField):
    default_error_messages: _ErrorMessagesT
    base_field: type[forms.Field]
    range_type: type[Range]
