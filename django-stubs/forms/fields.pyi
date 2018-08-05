from collections import OrderedDict
from datetime import date, datetime, time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from django.db.models.base import Model
from django.db.models.fields.files import FieldFile
from django.forms.boundfield import BoundField
from django.forms.forms import BaseForm
from django.forms.widgets import Widget


class Field:
    initial: None
    label: None
    required: bool
    widget: Any = ...
    hidden_widget: Any = ...
    default_validators: Any = ...
    default_error_messages: Any = ...
    empty_values: Any = ...
    show_hidden_initial: bool = ...
    help_text: str = ...
    disabled: bool = ...
    label_suffix: None = ...
    localize: bool = ...
    error_messages: Any = ...
    validators: Any = ...
    def __init__(
        self,
        *,
        required: bool = ...,
        widget: Optional[Any] = ...,
        label: Optional[Any] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        error_messages: Optional[Any] = ...,
        show_hidden_initial: bool = ...,
        validators: Any = ...,
        localize: bool = ...,
        disabled: bool = ...,
        label_suffix: Optional[Any] = ...
    ) -> None: ...
    def prepare_value(self, value: Any) -> Any: ...
    def to_python(
        self, value: Optional[Union[bool, List[str], List[None], str]]
    ) -> Optional[Union[bool, List[str], List[None], str]]: ...
    def validate(self, value: Optional[Union[Model, int, str]]) -> None: ...
    def run_validators(self, value: Any) -> None: ...
    def clean(
        self, value: Optional[Union[List[int], int, str]]
    ) -> Optional[Union[Model, int, str]]: ...
    def bound_data(
        self,
        data: Optional[Union[str, bool, List[str]]],
        initial: Optional[Union[int, str, datetime]],
    ) -> Optional[Union[str, bool, List[str]]]: ...
    def widget_attrs(self, widget: Widget) -> Dict[Any, Any]: ...
    def has_changed(
        self,
        initial: Optional[Union[time, int, date, str]],
        data: Optional[str],
    ) -> bool: ...
    def get_bound_field(
        self, form: BaseForm, field_name: str
    ) -> BoundField: ...
    def __deepcopy__(self, memo: Dict[int, Any]) -> Field: ...

class CharField(Field):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[str, Callable]]
    label: Optional[str]
    label_suffix: Optional[str]
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[
        Union[
            django.core.validators.BaseValidator,
            django.core.validators.ProhibitNullCharactersValidator,
        ]
    ]
    widget: django.forms.widgets.TextInput
    max_length: Optional[Union[str, int]] = ...
    min_length: Optional[Union[str, int]] = ...
    strip: bool = ...
    empty_value: Optional[str] = ...
    def __init__(
        self,
        *,
        max_length: Optional[Any] = ...,
        min_length: Optional[Any] = ...,
        strip: bool = ...,
        empty_value: str = ...,
        **kwargs: Any
    ) -> None: ...
    def to_python(
        self, value: Optional[Union[str, List[int], int]]
    ) -> Optional[str]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, str]: ...

class IntegerField(Field):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[Callable, int]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_value: Optional[int]
    min_value: Optional[int]
    required: bool
    show_hidden_initial: bool
    validators: List[django.core.validators.BaseValidator]
    widget: django.forms.widgets.NumberInput = ...
    default_error_messages: Any = ...
    re_decimal: Any = ...
    def __init__(
        self,
        *,
        max_value: Optional[Any] = ...,
        min_value: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def to_python(self, value: str) -> int: ...
    def widget_attrs(self, widget: Widget) -> Dict[Any, Any]: ...

class FloatField(IntegerField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_value: Optional[float]
    min_value: Optional[float]
    required: bool
    show_hidden_initial: bool
    validators: List[django.core.validators.BaseValidator]
    widget: django.forms.widgets.NumberInput
    default_error_messages: Any = ...
    def to_python(self, value: Any): ...
    def validate(self, value: Any): ...
    def widget_attrs(self, widget: Any): ...

class DecimalField(IntegerField):
    decimal_places: Optional[int]
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_digits: Optional[int]
    max_value: Optional[Union[decimal.Decimal, int]]
    min_value: Optional[Union[decimal.Decimal, int]]
    required: bool
    show_hidden_initial: bool
    validators: List[
        Union[
            django.core.validators.BaseValidator,
            django.core.validators.DecimalValidator,
        ]
    ]
    widget: django.forms.widgets.NumberInput
    default_error_messages: Any = ...
    def __init__(
        self,
        *,
        max_value: Optional[Any] = ...,
        min_value: Optional[Any] = ...,
        max_digits: Optional[Any] = ...,
        decimal_places: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def to_python(self, value: Any): ...
    def validate(self, value: Any): ...
    def widget_attrs(self, widget: Any): ...

class BaseTemporalField(Field):
    input_formats: Any = ...
    def __init__(
        self, *, input_formats: Optional[Any] = ..., **kwargs: Any
    ) -> None: ...
    def to_python(self, value: Any): ...
    def strptime(self, value: Any, format: Any) -> None: ...

class DateField(BaseTemporalField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[Callable, datetime.date]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.DateInput = ...
    input_formats: Any = ...
    default_error_messages: Any = ...
    def to_python(self, value: date) -> date: ...
    def strptime(self, value: Any, format: Any): ...

class TimeField(BaseTemporalField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Callable]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.TimeInput = ...
    input_formats: Any = ...
    default_error_messages: Any = ...
    def to_python(self, value: time) -> time: ...
    def strptime(self, value: Any, format: Any): ...

class DateTimeField(BaseTemporalField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[Callable, datetime.datetime]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.DateTimeInput = ...
    input_formats: Any = ...
    default_error_messages: Any = ...
    def prepare_value(self, value: Any): ...
    def to_python(self, value: Any): ...
    def strptime(self, value: Any, format: Any): ...

class DurationField(Field):
    disabled: bool
    help_text: str
    initial: Optional[datetime.timedelta]
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    default_error_messages: Any = ...
    def prepare_value(self, value: Any): ...
    def to_python(self, value: Any): ...

class RegexField(CharField):
    disabled: bool
    empty_value: str
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    max_length: Optional[int]
    min_length: Optional[int]
    required: bool
    show_hidden_initial: bool
    strip: bool
    validators: List[
        Union[
            django.core.validators.BaseValidator,
            django.core.validators.ProhibitNullCharactersValidator,
            django.core.validators.RegexValidator,
        ]
    ]
    widget: django.forms.widgets.TextInput
    def __init__(self, regex: Any, **kwargs: Any) -> None: ...
    regex: Any = ...

class EmailField(CharField):
    disabled: bool
    empty_value: Optional[str]
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_length: Optional[int]
    min_length: Optional[int]
    required: bool
    show_hidden_initial: bool
    strip: bool
    validators: List[
        Union[
            django.core.validators.EmailValidator,
            django.core.validators.BaseValidator,
            django.core.validators.ProhibitNullCharactersValidator,
        ]
    ]
    widget: django.forms.widgets.EmailInput = ...
    default_validators: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...

class FileField(Field):
    disabled: bool
    help_text: str
    initial: Optional[Union[Callable, str]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    widget: Any = ...
    default_error_messages: Any = ...
    max_length: Optional[int] = ...
    allow_empty_file: bool = ...
    def __init__(
        self,
        *,
        max_length: Optional[Any] = ...,
        allow_empty_file: bool = ...,
        **kwargs: Any
    ) -> None: ...
    def to_python(self, data: None) -> None: ...
    def clean(
        self, data: None, initial: Optional[FieldFile] = ...
    ) -> FieldFile: ...
    def bound_data(
        self, data: None, initial: Optional[FieldFile]
    ) -> Optional[FieldFile]: ...
    def has_changed(self, initial: Optional[FieldFile], data: None) -> bool: ...

class ImageField(FileField):
    allow_empty_file: bool
    disabled: bool
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_length: Optional[int]
    required: bool
    show_hidden_initial: bool
    default_validators: Any = ...
    default_error_messages: Any = ...
    def to_python(self, data: Any): ...
    def widget_attrs(self, widget: Any): ...

class URLField(CharField):
    disabled: bool
    empty_value: Optional[str]
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_length: Optional[int]
    min_length: Optional[int]
    required: bool
    show_hidden_initial: bool
    strip: bool
    validators: List[
        Union[
            django.core.validators.URLValidator,
            django.core.validators.MaxLengthValidator,
            django.core.validators.ProhibitNullCharactersValidator,
        ]
    ]
    widget: django.forms.widgets.URLInput = ...
    default_error_messages: Any = ...
    default_validators: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    def to_python(self, value: None) -> str: ...

class BooleanField(Field):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[int]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.CheckboxInput = ...
    def to_python(self, value: Optional[Union[str, int]]) -> bool: ...
    def validate(self, value: bool) -> None: ...
    def has_changed(
        self, initial: Optional[Union[bool, str]], data: Optional[str]
    ) -> bool: ...

class NullBooleanField(BooleanField):
    disabled: bool
    help_text: str
    initial: Optional[bool]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    widget: Any = ...
    def to_python(self, value: None) -> None: ...
    def validate(self, value: None) -> None: ...

class CallableChoiceIterator:
    choices_func: Callable = ...
    def __init__(self, choices_func: Callable) -> None: ...
    def __iter__(self) -> None: ...

class ChoiceField(Field):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.Select = ...
    default_error_messages: Any = ...
    choices: Any = ...
    def __init__(self, *, choices: Any = ..., **kwargs: Any) -> None: ...
    def __deepcopy__(self, memo: Dict[int, Any]) -> ChoiceField: ...
    def to_python(self, value: Optional[Union[str, int]]) -> str: ...
    def validate(self, value: str) -> None: ...
    def valid_value(self, value: str) -> bool: ...

class TypedChoiceField(ChoiceField):
    disabled: bool
    help_text: str
    initial: Optional[Union[Callable, int]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    coerce: Union[Callable, Type[Union[str, float, int]]] = ...
    empty_value: Optional[str] = ...
    def __init__(
        self, *, coerce: Any = ..., empty_value: str = ..., **kwargs: Any
    ) -> None: ...
    def clean(self, value: str) -> Optional[Union[str, int]]: ...

class MultipleChoiceField(ChoiceField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Callable]
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    hidden_widget: Any = ...
    widget: django.forms.widgets.SelectMultiple = ...
    default_error_messages: Any = ...
    def to_python(self, value: Any): ...
    def validate(self, value: Any) -> None: ...
    def has_changed(self, initial: Any, data: Any): ...

class TypedMultipleChoiceField(MultipleChoiceField):
    disabled: bool
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    coerce: Union[Callable, Type[Union[int, float]]] = ...
    empty_value: Optional[List[Any]] = ...
    def __init__(self, *, coerce: Any = ..., **kwargs: Any) -> None: ...
    def clean(self, value: Any): ...
    def validate(self, value: Any) -> None: ...

class ComboField(Field):
    disabled: bool
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    fields: Any = ...
    def __init__(self, fields: List[CharField], **kwargs: Any) -> None: ...
    def clean(self, value: Optional[str]) -> str: ...

class MultiValueField(Field):
    disabled: bool
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    default_error_messages: Any = ...
    require_all_fields: bool = ...
    fields: Any = ...
    def __init__(
        self,
        fields: Tuple[DateField, TimeField],
        *,
        require_all_fields: bool = ...,
        **kwargs: Any
    ) -> None: ...
    def __deepcopy__(
        self,
        memo: Dict[
            int,
            Union[
                OrderedDict,
                Field,
                Widget,
                List[Union[Widget, Field]],
                List[Union[Widget, CharField]],
            ],
        ],
    ) -> SplitDateTimeField: ...
    def validate(self, value: Any) -> None: ...
    def clean(self, value: Any): ...
    def compress(self, data_list: Any) -> None: ...
    def has_changed(
        self, initial: Optional[Union[List[None], datetime]], data: List[str]
    ) -> bool: ...

class FilePathField(ChoiceField):
    allow_files: bool
    allow_folders: bool
    disabled: bool
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    match: Optional[str]
    path: str
    recursive: bool
    required: bool
    show_hidden_initial: bool
    choices: Any = ...
    match_re: Any = ...
    def __init__(
        self,
        path: Any,
        *,
        match: Optional[Any] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        **kwargs: Any
    ) -> None: ...

class SplitDateTimeField(MultiValueField):
    disabled: bool
    help_text: str
    initial: Optional[Union[Callable, datetime.datetime]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    require_all_fields: bool
    required: bool
    show_hidden_initial: bool
    widget: Any = ...
    hidden_widget: Any = ...
    default_error_messages: Any = ...
    def __init__(
        self,
        *,
        input_date_formats: Optional[Any] = ...,
        input_time_formats: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def compress(self, data_list: Any): ...

class GenericIPAddressField(CharField):
    disabled: bool
    empty_value: str
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    max_length: None
    min_length: None
    required: bool
    show_hidden_initial: bool
    strip: bool
    validators: List[Callable]
    widget: django.forms.widgets.TextInput
    unpack_ipv4: bool = ...
    default_validators: List[Callable] = ...
    def __init__(
        self, *, protocol: str = ..., unpack_ipv4: bool = ..., **kwargs: Any
    ) -> None: ...
    def to_python(self, value: Any): ...

class SlugField(CharField):
    disabled: bool
    empty_value: str
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_length: Optional[int]
    min_length: None
    required: bool
    show_hidden_initial: bool
    strip: bool
    default_validators: List[django.core.validators.RegexValidator] = ...
    allow_unicode: bool = ...
    def __init__(self, *, allow_unicode: bool = ..., **kwargs: Any) -> None: ...

class UUIDField(CharField):
    disabled: bool
    empty_value: str
    help_text: str
    initial: Optional[Callable]
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_length: None
    min_length: None
    required: bool
    show_hidden_initial: bool
    strip: bool
    default_error_messages: Any = ...
    def prepare_value(self, value: Any): ...
    def to_python(self, value: Any): ...
