import datetime
from decimal import Decimal
from typing import Any, Collection, Dict, Iterator, List, Optional, Pattern, Protocol, Sequence, Tuple, Type, Union
from uuid import UUID

from django.core.files import File
from django.core.validators import _ValidatorCallable
from django.db.models.fields import _Choice, _ChoiceNamedGroup, _ChoicesCallable, _ErrorMessagesT, _FieldChoices
from django.forms.boundfield import BoundField
from django.forms.forms import BaseForm
from django.forms.widgets import ChoiceWidget, Widget
from django.utils.datastructures import _PropertyDescriptor

# Problem: attribute `widget` is always of type `Widget` after field instantiation.
# However, on class level it can be set to `Type[Widget]` too.
# If we annotate it as `Union[Widget, Type[Widget]]`, every code that uses field
# instances will not typecheck.
# If we annotate it as `Widget`, any widget subclasses that do e.g.
# `widget = Select` will not typecheck.
# `Any` gives too much freedom, but does not create false positives.
_ClassLevelWidgetT = Any

class Field:
    initial: Any
    label: Optional[str]
    required: bool
    widget: _ClassLevelWidgetT = ...
    hidden_widget: Type[Widget] = ...
    default_validators: List[_ValidatorCallable] = ...
    default_error_messages: _ErrorMessagesT = ...
    empty_values: Sequence[Any] = ...
    show_hidden_initial: bool = ...
    help_text: str = ...
    disabled: bool = ...
    label_suffix: Optional[str] = ...
    localize: bool = ...
    error_messages: _ErrorMessagesT = ...
    validators: List[_ValidatorCallable] = ...
    max_length: Optional[int] = ...
    def __init__(
        self,
        *,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def prepare_value(self, value: Any) -> Any: ...
    def to_python(self, value: Optional[Any]) -> Optional[Any]: ...
    def validate(self, value: Any) -> None: ...
    def run_validators(self, value: Any) -> None: ...
    def clean(self, value: Any) -> Any: ...
    def bound_data(self, data: Any, initial: Any) -> Any: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...
    def has_changed(self, initial: Optional[Any], data: Optional[Any]) -> bool: ...
    def get_bound_field(self, form: BaseForm, field_name: str) -> BoundField: ...
    def deconstruct(self) -> Any: ...

class CharField(Field):
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    strip: bool = ...
    empty_value: Optional[str] = ...
    def __init__(
        self,
        *,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        strip: bool = ...,
        empty_value: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Optional[Any]) -> Optional[str]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...

class IntegerField(Field):
    max_value: Optional[int]
    min_value: Optional[int]
    re_decimal: Any = ...
    def __init__(
        self,
        *,
        max_value: Optional[int] = ...,
        min_value: Optional[int] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Optional[Any]) -> Optional[int]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...

class FloatField(IntegerField):
    def to_python(self, value: Optional[Any]) -> Optional[float]: ...  # type: ignore
    def validate(self, value: float) -> None: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...

class DecimalField(IntegerField):
    decimal_places: Optional[int]
    max_digits: Optional[int]
    def __init__(
        self,
        *,
        max_value: Union[Decimal, int, float, None] = ...,
        min_value: Union[Decimal, int, float, None] = ...,
        max_digits: Optional[int] = ...,
        decimal_places: Optional[int] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Optional[Any]) -> Optional[Decimal]: ...  # type: ignore
    def validate(self, value: Decimal) -> None: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...

class BaseTemporalField(Field):
    input_formats: Any = ...
    def __init__(
        self,
        *,
        input_formats: Optional[Any] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Optional[str]) -> Optional[Any]: ...
    def strptime(self, value: str, format: str) -> Any: ...

class DateField(BaseTemporalField):
    def to_python(self, value: Union[None, str, datetime.datetime, datetime.date]) -> Optional[datetime.date]: ...
    def strptime(self, value: str, format: str) -> datetime.date: ...

class TimeField(BaseTemporalField):
    def to_python(self, value: Union[None, str, datetime.time]) -> Optional[datetime.time]: ...
    def strptime(self, value: str, format: str) -> datetime.time: ...

class DateTimeFormatsIterator:
    def __iter__(self) -> Iterator[str]: ...

class DateTimeField(BaseTemporalField):
    def to_python(self, value: Union[None, str, datetime.datetime, datetime.date]) -> Optional[datetime.datetime]: ...
    def strptime(self, value: str, format: str) -> datetime.datetime: ...

class DurationField(Field):
    def prepare_value(self, value: Optional[Union[datetime.timedelta, str]]) -> Optional[str]: ...
    def to_python(self, value: Optional[Any]) -> Optional[datetime.timedelta]: ...

class RegexField(CharField):
    regex: _PropertyDescriptor[Union[str, Pattern[str]], Pattern[str]] = ...
    def __init__(
        self,
        regex: Union[str, Pattern[str]],
        *,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        strip: bool = ...,
        empty_value: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...

class EmailField(CharField):
    def __init__(
        self,
        *,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        strip: bool = ...,
        empty_value: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...

class FileField(Field):
    allow_empty_file: bool = ...
    def __init__(
        self,
        *,
        max_length: Optional[int] = ...,
        allow_empty_file: bool = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def clean(self, data: Any, initial: Optional[Any] = ...) -> Any: ...
    def to_python(self, data: Optional[File]) -> Optional[File]: ...
    def bound_data(self, data: Optional[Any], initial: Any) -> Any: ...
    def has_changed(self, initial: Optional[Any], data: Optional[Any]) -> bool: ...

class ImageField(FileField):
    def to_python(self, data: Optional[File]) -> Optional[File]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Any]: ...

class URLField(CharField):
    def __init__(
        self,
        *,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        strip: bool = ...,
        empty_value: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Optional[Any]) -> Optional[str]: ...

class BooleanField(Field):
    def to_python(self, value: Optional[Any]) -> bool: ...
    def validate(self, value: Any) -> None: ...
    def has_changed(self, initial: Optional[Any], data: Optional[Any]) -> bool: ...

class NullBooleanField(BooleanField):
    def to_python(self, value: Optional[Any]) -> Optional[bool]: ...  # type: ignore
    def validate(self, value: Any) -> None: ...

class CallableChoiceIterator:
    choices_func: _ChoicesCallable = ...
    def __init__(self, choices_func: _ChoicesCallable) -> None: ...
    def __iter__(self) -> Iterator[Union[_Choice, _ChoiceNamedGroup]]: ...

class ChoiceField(Field):
    choices: _PropertyDescriptor[
        Union[_FieldChoices, _ChoicesCallable, CallableChoiceIterator],
        Union[_FieldChoices, CallableChoiceIterator],
    ] = ...
    widget: _ClassLevelWidgetT
    def __init__(
        self,
        *,
        choices: Union[_FieldChoices, _ChoicesCallable] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    # Real return type of `to_python` is `str`, but it results in errors when
    # subclassing `ModelChoiceField`: `# type: ignore[override]` is not inherited
    def to_python(self, value: Optional[Any]) -> Any: ...
    def validate(self, value: Any) -> None: ...
    def valid_value(self, value: Any) -> bool: ...

class _CoerceCallable(Protocol):
    def __call__(self, __value: Any) -> Any: ...

class TypedChoiceField(ChoiceField):
    coerce: _CoerceCallable = ...
    empty_value: Optional[str] = ...
    def __init__(
        self,
        *,
        coerce: _CoerceCallable = ...,
        empty_value: Optional[str] = ...,
        choices: Union[_FieldChoices, _ChoicesCallable] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def clean(self, value: Any) -> Any: ...

class MultipleChoiceField(ChoiceField):
    def to_python(self, value: Optional[Any]) -> List[str]: ...
    def validate(self, value: Any) -> None: ...
    def has_changed(self, initial: Optional[Collection[Any]], data: Optional[Collection[Any]]) -> bool: ...

class TypedMultipleChoiceField(MultipleChoiceField):
    coerce: _CoerceCallable = ...
    empty_value: Optional[List[Any]] = ...
    def __init__(
        self,
        *,
        coerce: _CoerceCallable = ...,
        empty_value: Optional[List[Any]] = ...,
        choices: Union[_FieldChoices, _ChoicesCallable] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def clean(self, value: Any) -> Any: ...
    def validate(self, value: Any) -> None: ...

class ComboField(Field):
    fields: Sequence[Field] = ...
    def __init__(
        self,
        fields: Sequence[Field],
        *,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def clean(self, value: Any) -> Any: ...

class MultiValueField(Field):
    require_all_fields: bool = ...
    fields: Sequence[Field] = ...
    def __init__(
        self,
        fields: Sequence[Field],
        *,
        require_all_fields: bool = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def compress(self, data_list: Any) -> Any: ...
    def has_changed(self, initial: Optional[Any], data: Optional[Any]) -> bool: ...
    def clean(self, value: Any) -> Any: ...
    def validate(self, value: Any) -> None: ...

class FilePathField(ChoiceField):
    allow_files: bool
    allow_folders: bool
    match: Optional[str]
    path: str
    recursive: bool
    match_re: Optional[Pattern[str]] = ...
    def __init__(
        self,
        path: str,
        *,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        choices: Union[_FieldChoices, _ChoicesCallable] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...

class SplitDateTimeField(MultiValueField):
    def __init__(
        self,
        *,
        input_date_formats: Optional[Any] = ...,
        input_time_formats: Optional[Any] = ...,
        fields: Sequence[Field] = ...,
        require_all_fields: bool = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def compress(self, data_list: Optional[Tuple[datetime.date, datetime.time]]) -> Optional[datetime.datetime]: ...

class GenericIPAddressField(CharField):
    unpack_ipv4: bool = ...
    def __init__(
        self,
        *,
        protocol: str = ...,
        unpack_ipv4: bool = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...
    def to_python(self, value: Any) -> str: ...

class SlugField(CharField):
    allow_unicode: bool = ...
    def __init__(
        self,
        *,
        allow_unicode: bool = ...,
        max_length: Optional[Any] = ...,
        min_length: Optional[Any] = ...,
        strip: bool = ...,
        empty_value: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        show_hidden_initial: bool = ...,
        validators: Sequence[_ValidatorCallable] = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[str] = ...,
    ) -> None: ...

class UUIDField(CharField):
    def prepare_value(self, value: Optional[Any]) -> Optional[Any]: ...
    def to_python(self, value: Any) -> Optional[UUID]: ...  # type: ignore

class InvalidJSONInput(str): ...
class JSONString(str): ...

class JSONField(CharField):
    default_error_messages: _ErrorMessagesT = ...
    widget: _ClassLevelWidgetT = ...
    encoder: Any = ...
    decoder: Any = ...
    def __init__(self, encoder: Optional[Any] = ..., decoder: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def to_python(self, value: Any) -> Any: ...
    def bound_data(self, data: Any, initial: Any) -> Any: ...
    def prepare_value(self, value: Any) -> str: ...
    def has_changed(self, initial: Optional[Any], data: Optional[Any]) -> bool: ...
