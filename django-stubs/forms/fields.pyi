from collections import OrderedDict
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID

from django.contrib.admin.widgets import (AdminEmailInputWidget,
                                          AdminIntegerFieldWidget,
                                          AdminSplitDateTime,
                                          AdminTextareaWidget,
                                          AdminTextInputWidget,
                                          AdminURLFieldWidget,
                                          RelatedFieldWidgetWrapper)
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       ReadOnlyPasswordHashWidget)
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.base import Model
from django.db.models.fields.files import FieldFile
from django.forms.boundfield import BoundField
from django.forms.forms import BaseForm
from django.forms.models import ModelChoiceField
from django.forms.widgets import (CheckboxInput, ClearableFileInput,
                                  EmailInput, HiddenInput, Input, MultiWidget,
                                  NumberInput, PasswordInput, RadioSelect,
                                  Select, SplitDateTimeWidget, Textarea,
                                  TextInput, Widget)


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
    def prepare_value(
        self,
        value: Optional[
            Union[
                Dict[str, str],
                List[Union[List[str], str]],
                date,
                time,
                Decimal,
                File,
                float,
                int,
                str,
                UUID,
            ]
        ],
    ) -> Optional[
        Union[
            Dict[str, str],
            List[Union[List[str], str]],
            date,
            time,
            Decimal,
            File,
            float,
            int,
            str,
            UUID,
        ]
    ]: ...
    def to_python(
        self,
        value: Optional[
            Union[List[None], List[str], datetime, float, int, str]
        ],
    ) -> Optional[Union[List[None], List[str], datetime, float, int, str]]: ...
    def validate(
        self,
        value: Optional[
            Union[
                date,
                time,
                timedelta,
                Decimal,
                SimpleUploadedFile,
                Model,
                float,
                int,
                str,
                UUID,
            ]
        ],
    ) -> None: ...
    def run_validators(
        self,
        value: Optional[
            Union[
                List[Union[int, str]],
                date,
                time,
                timedelta,
                Decimal,
                SimpleUploadedFile,
                Model,
                float,
                int,
                str,
                UUID,
            ]
        ],
    ) -> None: ...
    def clean(
        self,
        value: Optional[
            Union[
                Dict[Any, Any],
                List[Dict[str, str]],
                List[List[str]],
                List[Union[int, str]],
                Tuple,
                date,
                time,
                Decimal,
                SimpleUploadedFile,
                float,
                int,
                str,
            ]
        ],
    ) -> Optional[
        Union[
            List[str],
            date,
            time,
            timedelta,
            Decimal,
            SimpleUploadedFile,
            Model,
            float,
            int,
            str,
            UUID,
        ]
    ]: ...
    def bound_data(
        self,
        data: Optional[
            Union[List[Union[List[str], str]], datetime, Decimal, int, str]
        ],
        initial: Optional[Union[List[str], date, float, int, str, UUID]],
    ) -> Optional[
        Union[List[Union[List[str], str]], date, Decimal, int, str]
    ]: ...
    def widget_attrs(self, widget: Widget) -> Dict[Any, Any]: ...
    def has_changed(
        self,
        initial: Optional[Union[date, time, Decimal, float, int, str]],
        data: Optional[str],
    ) -> bool: ...
    def get_bound_field(
        self, form: BaseForm, field_name: str
    ) -> BoundField: ...
    def __deepcopy__(
        self,
        memo: Union[
            Dict[
                int,
                Union[
                    List[Tuple[str, str]],
                    List[
                        Union[
                            List[Tuple[str, str]],
                            CharField,
                            ChoiceField,
                            IntegerField,
                            EmailInput,
                            NumberInput,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            CharField,
                            DateField,
                            EmailInput,
                            PasswordInput,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[CharField, DateTimeField, DecimalField, TextInput]
                    ],
                    List[Union[CharField, HiddenInput, TextInput]],
                    List[
                        Union[DateTimeField, TimeField, HiddenInput, TextInput]
                    ],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
            Dict[
                int,
                Union[
                    List[Tuple[str, str]],
                    List[
                        Union[
                            List[Tuple[str, str]],
                            CharField,
                            DateField,
                            TypedChoiceField,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            AdminIntegerFieldWidget,
                            RelatedFieldWidgetWrapper,
                            IntegerField,
                            ModelChoiceField,
                            Select,
                        ]
                    ],
                    List[
                        Union[
                            BooleanField,
                            CharField,
                            CheckboxInput,
                            TextInput,
                            Textarea,
                        ]
                    ],
                    List[Union[NullBooleanField, RadioSelect]],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
            Dict[
                int,
                Union[
                    List[
                        Union[
                            List[Any],
                            List[Union[Tuple[int, str], Tuple[str, str]]],
                            AdminSplitDateTime,
                            RelatedFieldWidgetWrapper,
                            ReadOnlyPasswordHashField,
                            ReadOnlyPasswordHashWidget,
                            BooleanField,
                            CharField,
                            ChoiceField,
                            SplitDateTimeField,
                            CheckboxInput,
                            EmailInput,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            List[Tuple[str, str]],
                            RelatedFieldWidgetWrapper,
                            CharField,
                            ModelChoiceField,
                            MultiWidget,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[Union[Tuple[int, str], Tuple[str, str]]],
                    List[
                        Union[
                            AdminTextareaWidget,
                            AdminURLFieldWidget,
                            CharField,
                            DateField,
                            IntegerField,
                            TimeField,
                            ModelChoiceField,
                            NumberInput,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            RelatedFieldWidgetWrapper,
                            CharField,
                            DateField,
                            SplitDateTimeField,
                            ModelChoiceField,
                            PasswordInput,
                            Select,
                            SplitDateTimeWidget,
                            TextInput,
                            Textarea,
                        ]
                    ],
                    List[
                        Union[
                            ReadOnlyPasswordHashField,
                            ReadOnlyPasswordHashWidget,
                            BooleanField,
                            CharField,
                            DateTimeField,
                            ModelChoiceField,
                            CheckboxInput,
                            EmailInput,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            CharField,
                            DateField,
                            TimeField,
                            ModelChoiceField,
                            EmailInput,
                            MultiWidget,
                            TextInput,
                            Textarea,
                        ]
                    ],
                    List[Union[NullBooleanField, HiddenInput]],
                    List[Union[ModelChoiceField, RadioSelect]],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
            Dict[
                int,
                Union[
                    List[
                        Union[
                            List[Union[Tuple[int, str], Tuple[str, str]]],
                            AdminIntegerFieldWidget,
                            AdminTextInputWidget,
                            CharField,
                            IntegerField,
                            TypedChoiceField,
                            Select,
                        ]
                    ],
                    List[
                        Union[
                            List[Union[Tuple[int, str], Tuple[str, str]]],
                            RelatedFieldWidgetWrapper,
                            TypedChoiceField,
                            ModelChoiceField,
                            Select,
                        ]
                    ],
                    List[Union[Tuple[int, str], Tuple[str, str]]],
                    List[
                        Union[
                            CharField, FileField, ClearableFileInput, TextInput
                        ]
                    ],
                    List[
                        Union[
                            DateField,
                            DateTimeField,
                            IntegerField,
                            TimeField,
                            HiddenInput,
                            TextInput,
                        ]
                    ],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
        ],
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
    validators: List[
        Union[
            django.core.validators.MaxLengthValidator,
            django.core.validators.MinLengthValidator,
            django.core.validators.ProhibitNullCharactersValidator,
        ]
    ]
    widget: django.forms.widgets.TextInput
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
    def to_python(
        self, value: Optional[Union[List[int], Tuple, int, str]]
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
    validators: List[
        Union[
            django.core.validators.MaxValueValidator,
            django.core.validators.MinValueValidator,
        ]
    ]
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
    def to_python(
        self, value: Optional[Union[float, int, str]]
    ) -> Optional[int]: ...
    def widget_attrs(
        self, widget: Widget
    ) -> Union[Dict[str, Decimal], Dict[str, float], Dict[str, int]]: ...

class FloatField(IntegerField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: None
    label: Optional[str]
    label_suffix: None
    localize: bool
    max_value: Optional[Union[float, int]]
    min_value: Optional[Union[float, int]]
    required: bool
    show_hidden_initial: bool
    validators: List[
        Union[
            django.core.validators.MaxValueValidator,
            django.core.validators.MinValueValidator,
        ]
    ]
    widget: django.forms.widgets.NumberInput
    default_error_messages: Any = ...
    def to_python(
        self, value: Optional[Union[float, int, str]]
    ) -> Optional[float]: ...
    def validate(self, value: Optional[float]) -> None: ...
    def widget_attrs(
        self, widget: Input
    ) -> Union[Dict[str, Union[float, str]], Dict[str, Union[int, str]]]: ...

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
            django.core.validators.DecimalValidator,
            django.core.validators.MaxValueValidator,
            django.core.validators.MinValueValidator,
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
    def to_python(
        self, value: Optional[Union[Decimal, float, str]]
    ) -> Optional[Decimal]: ...
    def validate(self, value: Optional[Decimal]) -> None: ...
    def widget_attrs(
        self, widget: Widget
    ) -> Union[Dict[str, Union[Decimal, str]], Dict[str, Union[int, str]]]: ...

class BaseTemporalField(Field):
    input_formats: Any = ...
    def __init__(
        self, *, input_formats: Optional[Any] = ..., **kwargs: Any
    ) -> None: ...
    def to_python(self, value: str) -> Union[date, time]: ...
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
    def to_python(
        self, value: Optional[Union[date, str]]
    ) -> Optional[date]: ...
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
    validators: List[Any]
    widget: django.forms.widgets.TimeInput = ...
    input_formats: Any = ...
    default_error_messages: Any = ...
    def to_python(
        self, value: Optional[Union[time, str]]
    ) -> Optional[time]: ...
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
    validators: List[Any]
    widget: django.forms.widgets.DateTimeInput = ...
    input_formats: Any = ...
    default_error_messages: Any = ...
    def prepare_value(
        self, value: Optional[datetime]
    ) -> Optional[datetime]: ...
    def to_python(
        self, value: Optional[Union[date, str]]
    ) -> Optional[datetime]: ...
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
    def prepare_value(
        self, value: Optional[Union[timedelta, str]]
    ) -> Optional[str]: ...
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
    validators: List[
        Union[
            django.core.validators.MaxLengthValidator,
            django.core.validators.MinLengthValidator,
            django.core.validators.ProhibitNullCharactersValidator,
            django.core.validators.RegexValidator,
        ]
    ]
    widget: django.forms.widgets.TextInput
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
    validators: List[
        Union[
            django.core.validators.EmailValidator,
            django.core.validators.MaxLengthValidator,
            django.core.validators.MinLengthValidator,
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
    def to_python(
        self, data: Optional[Union[SimpleUploadedFile, str]]
    ) -> Optional[SimpleUploadedFile]: ...
    def clean(
        self, data: Any, initial: Optional[Union[FieldFile, str]] = ...
    ) -> Optional[Union[bool, File, str]]: ...
    def bound_data(
        self, data: Any, initial: Optional[FieldFile]
    ) -> Optional[Union[File, str]]: ...
    def has_changed(
        self,
        initial: Optional[Union[FieldFile, str]],
        data: Optional[Union[Dict[str, str], str]],
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
    def to_python(
        self, data: Optional[SimpleUploadedFile]
    ) -> Optional[SimpleUploadedFile]: ...
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
    validators: List[
        Union[
            django.core.validators.MaxLengthValidator,
            django.core.validators.ProhibitNullCharactersValidator,
            django.core.validators.URLValidator,
        ]
    ]
    widget: django.forms.widgets.URLInput = ...
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
    validators: List[Any]
    widget: django.forms.widgets.CheckboxInput = ...
    def to_python(self, value: Optional[Union[int, str]]) -> bool: ...
    def validate(self, value: bool) -> None: ...
    def has_changed(
        self,
        initial: Optional[Union[bool, str]],
        data: Optional[Union[bool, str]],
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
    def to_python(
        self, value: Optional[Union[bool, str]]
    ) -> Optional[bool]: ...
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
    validators: List[Any]
    widget: django.forms.widgets.Select = ...
    default_error_messages: Any = ...
    choices: Any = ...
    def __init__(self, *, choices: Any = ..., **kwargs: Any) -> None: ...
    def __deepcopy__(
        self,
        memo: Union[
            Dict[
                int,
                Union[
                    List[
                        Union[
                            List[Tuple[str, str]],
                            CharField,
                            ChoiceField,
                            IntegerField,
                            EmailInput,
                            NumberInput,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            List[Tuple[str, str]],
                            CharField,
                            DateField,
                            TypedChoiceField,
                            Select,
                            TextInput,
                        ]
                    ],
                    List[
                        Union[
                            List[Union[Tuple[int, str], Tuple[str, str]]],
                            RelatedFieldWidgetWrapper,
                            TypedChoiceField,
                            ModelChoiceField,
                            Select,
                        ]
                    ],
                    List[Union[Tuple[int, str], Tuple[str, str]]],
                    List[
                        Union[
                            CharField,
                            DateField,
                            ModelChoiceField,
                            Select,
                            TextInput,
                            Textarea,
                        ]
                    ],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
            Dict[
                int,
                Union[
                    List[Union[CharField, PasswordInput, TextInput]],
                    List[Union[MultiWidget, TextInput]],
                    OrderedDict,
                    Field,
                    Widget,
                ],
            ],
        ],
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
    coerce: Union[Callable, Type[Union[float, int, str]]] = ...
    empty_value: Optional[str] = ...
    def __init__(
        self, *, coerce: Any = ..., empty_value: str = ..., **kwargs: Any
    ) -> None: ...
    def clean(
        self, value: Optional[str]
    ) -> Optional[Union[Decimal, float, int, str]]: ...

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
    def to_python(
        self, value: Optional[Union[List[Union[int, str]], Tuple, str]]
    ) -> List[str]: ...
    def validate(self, value: List[str]) -> None: ...
    def has_changed(
        self,
        initial: Optional[Union[List[int], List[str], str]],
        data: Optional[Union[List[str], str]],
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
    coerce: Union[Callable, Type[Union[float, int]]] = ...
    empty_value: Optional[List[Any]] = ...
    def __init__(self, *, coerce: Any = ..., **kwargs: Any) -> None: ...
    def clean(
        self, value: List[str]
    ) -> Optional[Union[List[Decimal], List[float], List[int]]]: ...
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
    def __init__(
        self,
        fields: Tuple[Field, Field],
        *,
        require_all_fields: bool = ...,
        **kwargs: Any
    ) -> None: ...
    def __deepcopy__(
        self,
        memo: Dict[
            int,
            Union[
                List[Tuple[str, str]],
                List[
                    Union[
                        List[Tuple[str, str]],
                        AdminEmailInputWidget,
                        RelatedFieldWidgetWrapper,
                        ReadOnlyPasswordHashField,
                        ReadOnlyPasswordHashWidget,
                        BooleanField,
                        CharField,
                        SplitDateTimeField,
                        ModelChoiceField,
                        CheckboxInput,
                        MultiWidget,
                        Select,
                        TextInput,
                    ]
                ],
                List[
                    Union[AdminTextInputWidget, AdminTextareaWidget, CharField]
                ],
                OrderedDict,
                Field,
                Widget,
            ],
        ],
    ) -> MultiValueField: ...
    def validate(self, value: Union[datetime, str]) -> None: ...
    def clean(
        self,
        value: Optional[
            Union[
                List[None],
                List[Union[List[str], str]],
                List[Union[date, time]],
                datetime,
                str,
            ]
        ],
    ) -> Optional[Union[datetime, str]]: ...
    def compress(self, data_list: Any) -> None: ...
    def has_changed(
        self,
        initial: Optional[Union[List[None], List[str], datetime, str]],
        data: Union[List[None], List[Union[List[str], str]]],
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
    def compress(
        self,
        data_list: Union[
            List[Optional[date]], List[Optional[time]], List[Union[date, time]]
        ],
    ) -> Optional[datetime]: ...

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
    def prepare_value(self, value: UUID) -> str: ...
    def to_python(self, value: str) -> Optional[UUID]: ...
