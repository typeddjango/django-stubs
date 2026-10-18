from typing import Any, ClassVar

from django import forms
from django.db.models.fields import _ErrorMessagesDict
from django.forms.widgets import MultiWidget, _OptAttrs
from psycopg2.extras import Range
from typing_extensions import override

class RangeWidget(MultiWidget):
    def __init__(self, base_widget: forms.Widget | type[forms.Widget], attrs: _OptAttrs | None = None) -> None: ...
    @override
    def decompress(self, value: Any) -> tuple[Any | None, Any | None]: ...

class HiddenRangeWidget(RangeWidget):
    def __init__(self, attrs: _OptAttrs | None = None) -> None: ...

class BaseRangeField(forms.MultiValueField):
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: type[forms.Field]
    range_type: type[Range[Any]]
    hidden_widget: type[forms.Widget]
    def __init__(self, **kwargs: Any) -> None: ...
    @override
    def prepare_value(self, value: Any) -> Any: ...
    @override
    def compress(self, values: tuple[Any | None, Any | None]) -> Range[Any] | None: ...

class IntegerRangeField(BaseRangeField):
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: type[forms.Field]
    range_type: type[Range[Any]]

class DecimalRangeField(BaseRangeField):
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: type[forms.Field]
    range_type: type[Range[Any]]

class DateTimeRangeField(BaseRangeField):
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: type[forms.Field]
    range_type: type[Range[Any]]

class DateRangeField(BaseRangeField):
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: type[forms.Field]
    range_type: type[Range[Any]]

__all__ = [
    "BaseRangeField",
    "DateRangeField",
    "DateTimeRangeField",
    "DecimalRangeField",
    "HiddenRangeWidget",
    "IntegerRangeField",
    "RangeWidget",
]
