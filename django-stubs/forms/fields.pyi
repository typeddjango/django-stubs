from collections import OrderedDict
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Type
from uuid import UUID

from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import BaseValidator
from django.db.models.fields.files import FieldFile
from django.forms.boundfield import BoundField
from django.forms.forms import BaseForm
from django.forms.widgets import Input, Widget

class Field:
    initial: None
    label: None
    required: bool
    widget: Input = ...
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
    validators: List[BaseValidator] = ...
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
        self, value: Optional[Union[List[None], List[str], datetime, float, str]]
    ) -> Optional[Union[List[None], List[str], datetime, float, str]]: ...
    def validate(self, value: Any) -> None: ...
    def run_validators(self, value: Any) -> None: ...
    def clean(self, value: Any) -> Any: ...
    def bound_data(self, data: Any, initial: Any) -> Any: ...
    def widget_attrs(self, widget: Widget) -> Dict[Any, Any]: ...
    def has_changed(self, initial: Optional[Union[datetime, Decimal, float, str]], data: Optional[str]) -> bool: ...
    def get_bound_field(self, form: BaseForm, field_name: str) -> BoundField: ...
    def __deepcopy__(
        self, memo: Dict[int, Union[List[Tuple[Union[int, str], str]], List[Widget], OrderedDict, Field, Widget]]
    ) -> Field: ...

class CharField(Field):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[Callable, str]]
    label: Optional[str]
    label_suffix: Optional[str]
    localize: bool
    required: bool
    show_hidden_initial: bool
    max_length: Optional[Union[int, str]] = ...
    min_length: Optional[Union[int, str]] = ...
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
    def to_python(self, value: Optional[Union[List[int], Tuple, int, str]]) -> Optional[str]: ...
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
    default_error_messages: Any = ...
    re_decimal: Any = ...
    def __init__(self, *, max_value: Optional[Any] = ..., min_value: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def to_python(self, value: Optional[Union[float, str]]) -> Optional[int]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Union[Decimal, float]]: ...

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
    default_error_messages: Any = ...
    def to_python(self, value: Optional[Union[float, str]]) -> Optional[float]: ...
    def validate(self, value: Optional[float]) -> None: ...
    def widget_attrs(self, widget: Input) -> Dict[str, Union[float, str]]: ...

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
    def to_python(self, value: Optional[Union[Decimal, float, str]]) -> Optional[Decimal]: ...
    def validate(self, value: Optional[Decimal]) -> None: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, Union[Decimal, int, str]]: ...

class BaseTemporalField(Field):
    input_formats: Any = ...
    def __init__(self, *, input_formats: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def to_python(self, value: str) -> datetime: ...
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
    input_formats: Any = ...
    default_error_messages: Any = ...
    def to_python(self, value: Optional[Union[date, str]]) -> Optional[date]: ...
    def strptime(self, value: str, format: str) -> date: ...

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
    input_formats: Any = ...
    default_error_messages: Any = ...
    def to_python(self, value: Optional[Union[time, str]]) -> Optional[time]: ...
    def strptime(self, value: str, format: str) -> time: ...

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
    input_formats: Any = ...
    default_error_messages: Any = ...
    def prepare_value(self, value: Optional[datetime]) -> Optional[datetime]: ...
    def to_python(self, value: Optional[Union[date, str]]) -> Optional[datetime]: ...
    def strptime(self, value: str, format: str) -> datetime: ...

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
    def prepare_value(self, value: Optional[Union[timedelta, str]]) -> Optional[str]: ...
    def to_python(self, value: Union[int, str]) -> timedelta: ...

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
    def __init__(self, regex: str, **kwargs: Any) -> None: ...
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
    default_error_messages: Any = ...
    max_length: Optional[int] = ...
    allow_empty_file: bool = ...
    def __init__(self, *, max_length: Optional[Any] = ..., allow_empty_file: bool = ..., **kwargs: Any) -> None: ...
    def to_python(self, data: Optional[Union[SimpleUploadedFile, str]]) -> Optional[SimpleUploadedFile]: ...
    def clean(self, data: Any, initial: Optional[Union[FieldFile, str]] = ...) -> Optional[Union[bool, File, str]]: ...
    def bound_data(self, data: Any, initial: Optional[FieldFile]) -> Optional[Union[File, str]]: ...
    def has_changed(
        self, initial: Optional[Union[FieldFile, str]], data: Optional[Union[Dict[str, str], str]]
    ) -> bool: ...

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
    def to_python(self, data: Optional[SimpleUploadedFile]) -> Optional[SimpleUploadedFile]: ...
    def widget_attrs(self, widget: Widget) -> Dict[str, str]: ...

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
    default_error_messages: Any = ...
    default_validators: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    def to_python(self, value: Optional[Union[int, str]]) -> Optional[str]: ...

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
    def to_python(self, value: Optional[Union[int, str]]) -> bool: ...
    def validate(self, value: bool) -> None: ...
    def has_changed(self, initial: Optional[Union[bool, str]], data: Optional[Union[bool, str]]) -> bool: ...

class NullBooleanField(BooleanField):
    disabled: bool
    help_text: str
    initial: Optional[bool]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    def to_python(self, value: Optional[Union[bool, str]]) -> Optional[bool]: ...
    def validate(self, value: Optional[bool]) -> None: ...

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
    default_error_messages: Any = ...
    choices: Any = ...
    def __init__(self, *, choices: Any = ..., **kwargs: Any) -> None: ...
    def __deepcopy__(
        self, memo: Dict[int, Union[List[Tuple[Union[int, str], str]], List[Widget], OrderedDict, Field, Widget]]
    ) -> ChoiceField: ...
    def to_python(self, value: Optional[Union[int, str]]) -> str: ...
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
    coerce: Union[Callable, Type[Union[bool, float, str]]] = ...
    empty_value: Optional[str] = ...
    def __init__(self, *, coerce: Any = ..., empty_value: str = ..., **kwargs: Any) -> None: ...
    def clean(self, value: Optional[str]) -> Optional[Union[Decimal, float, str]]: ...

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
    hidden_widget: Any = ...
    default_error_messages: Any = ...
    def to_python(self, value: Optional[Union[List[Union[int, str]], Tuple, str]]) -> List[str]: ...
    def validate(self, value: List[str]) -> None: ...
    def has_changed(
        self, initial: Optional[Union[List[int], List[str], str]], data: Optional[Union[List[str], str]]
    ) -> bool: ...

class TypedMultipleChoiceField(MultipleChoiceField):
    disabled: bool
    help_text: str
    initial: None
    label: None
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    coerce: Union[Callable, Type[float]] = ...
    empty_value: Optional[List[Any]] = ...
    def __init__(self, *, coerce: Any = ..., **kwargs: Any) -> None: ...
    def clean(self, value: List[str]) -> Optional[Union[List[bool], List[Decimal], List[float]]]: ...
    def validate(self, value: List[str]) -> None: ...

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
    def __init__(self, fields: Tuple[Field, Field], *, require_all_fields: bool = ..., **kwargs: Any) -> None: ...
    def __deepcopy__(
        self, memo: Dict[int, Union[List[Tuple[str, str]], OrderedDict, Field, Widget]]
    ) -> MultiValueField: ...
    def validate(self, value: Union[datetime, str]) -> None: ...
    def clean(
        self, value: Optional[Union[List[None], List[datetime], List[str], datetime, str]]
    ) -> Optional[Union[datetime, str]]: ...
    def compress(self, data_list: Any) -> None: ...
    def has_changed(
        self, initial: Optional[Union[List[None], List[str], datetime, str]], data: Union[List[None], List[str]]
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
        path: str,
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
    hidden_widget: Any = ...
    default_error_messages: Any = ...
    def __init__(
        self, *, input_date_formats: Optional[Any] = ..., input_time_formats: Optional[Any] = ..., **kwargs: Any
    ) -> None: ...
    def compress(self, data_list: List[Optional[datetime]]) -> Optional[datetime]: ...

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
    unpack_ipv4: bool = ...
    default_validators: List[Callable] = ...
    def __init__(self, *, protocol: str = ..., unpack_ipv4: bool = ..., **kwargs: Any) -> None: ...
    def to_python(self, value: Optional[str]) -> str: ...

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
    def prepare_value(self, value: UUID) -> str: ...
    def to_python(self, value: str) -> Optional[UUID]: ...
