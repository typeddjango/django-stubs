from collections import OrderedDict
from datetime import date, datetime, time
from decimal import Decimal
from itertools import chain
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Type, Union)

from django.contrib.admin.options import BaseModelAdmin
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.forms.fields import Field
from django.forms.forms import BaseForm
from django.forms.renderers import EngineMixin
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import SafeText


class MediaOrderConflictWarning(RuntimeWarning): ...

class Media:
    def __init__(
        self,
        media: Optional[Type[Any]] = ...,
        css: Optional[Union[Dict[str, List[str]], Dict[str, Tuple[str]]]] = ...,
        js: Optional[Union[List[str], Tuple[str]]] = ...,
    ) -> None: ...
    def render(self) -> SafeText: ...
    def render_js(self) -> List[SafeText]: ...
    def render_css(self) -> chain: ...
    def absolute_path(self, path: str) -> str: ...
    def __getitem__(self, name: str) -> Media: ...
    @staticmethod
    def merge(
        list_1: Union[List[int], List[str], Tuple[str]],
        list_2: Union[List[int], List[str], Tuple[str]],
    ) -> Union[List[int], List[str]]: ...
    def __add__(self, other: Media) -> Media: ...

class MediaDefiningClass(type):
    def __new__(
        mcs: Type[MediaDefiningClass], name: str, bases: Tuple, attrs: Any
    ) -> Type[Union[BaseModelAdmin, BaseForm, Widget]]: ...

class Widget:
    needs_multipart_form: bool = ...
    is_localized: bool = ...
    is_required: bool = ...
    supports_microseconds: bool = ...
    attrs: Dict[Any, Any] = ...
    def __init__(
        self,
        attrs: Optional[
            Union[Dict[str, None], Dict[str, bool], Dict[str, float]]
        ] = ...,
    ) -> None: ...
    def __deepcopy__(
        self, memo: Dict[int, Union[Dict[Any, Any], List[Any]]]
    ) -> Widget: ...
    @property
    def is_hidden(self) -> bool: ...
    def subwidgets(
        self, name: str, value: None, attrs: Dict[str, bool] = ...
    ) -> Iterator[Dict[str, Optional[Union[Dict[str, bool], bool, str]]]]: ...
    def format_value(self, value: Any) -> Optional[str]: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str,
        Union[
            Dict[str, Optional[Union[Dict[str, None], bool, str]]],
            Dict[str, Optional[Union[Dict[str, bool], bool, str]]],
            Dict[str, Union[Dict[str, Union[int, str]], List[str], bool, str]],
            Dict[str, Union[Dict[str, str], List[int], bool, str]],
            Dict[str, Union[Dict[str, str], bool, FieldFile, str]],
        ],
    ]: ...
    def render(
        self,
        name: str,
        value: Any,
        attrs: Optional[Dict[str, Union[bool, str]]] = ...,
        renderer: Optional[EngineMixin] = ...,
    ) -> SafeText: ...
    def build_attrs(
        self,
        base_attrs: Dict[str, Union[float, str]],
        extra_attrs: Optional[Dict[str, Union[bool, str]]] = ...,
    ) -> Dict[str, Union[Decimal, float, str]]: ...
    def value_from_datadict(
        self,
        data: dict,
        files: Union[Dict[str, SimpleUploadedFile], MultiValueDict],
        name: str,
    ) -> Any: ...
    def value_omitted_from_data(
        self,
        data: Union[
            Dict[str, Optional[Union[List[int], date, int, str]]],
            Dict[str, Union[datetime, Decimal, int, str]],
            QueryDict,
        ],
        files: Union[Dict[str, SimpleUploadedFile], MultiValueDict],
        name: str,
    ) -> bool: ...
    def id_for_label(self, id_: str) -> str: ...
    def use_required_attribute(self, initial: Any) -> bool: ...

class Input(Widget):
    attrs: Dict[Any, Any]
    input_type: str = ...
    template_name: str = ...
    def __init__(
        self,
        attrs: Optional[
            Union[
                Dict[str, None],
                Dict[str, bool],
                Dict[str, float],
                Dict[str, str],
            ]
        ] = ...,
    ) -> None: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str,
        Union[
            Dict[str, Optional[Union[Dict[str, Union[int, str]], bool, str]]],
            Dict[str, Union[Dict[str, str], List[int], bool, str]],
            Dict[str, Union[Dict[str, str], List[str], bool, str]],
            Dict[str, Union[Dict[str, str], bool, FieldFile, str]],
        ],
    ]: ...

class TextInput(Input):
    attrs: Dict[str, Optional[bool]]
    is_localized: bool
    is_required: bool
    input_type: str = ...
    template_name: str = ...

class NumberInput(Input):
    attrs: Dict[str, Union[float, str]]
    is_required: bool
    input_type: str = ...
    template_name: str = ...

class EmailInput(Input):
    attrs: Dict[str, Union[bool, str]]
    is_required: bool
    input_type: str = ...
    template_name: str = ...

class URLInput(Input):
    attrs: Dict[str, str]
    is_required: bool
    input_type: str = ...
    template_name: str = ...

class PasswordInput(Input):
    attrs: Dict[str, Union[bool, str]]
    is_required: bool
    input_type: str = ...
    template_name: str = ...
    render_value: bool = ...
    def __init__(
        self, attrs: Optional[Dict[str, bool]] = ..., render_value: bool = ...
    ) -> None: ...
    def get_context(
        self,
        name: str,
        value: Optional[str],
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str, Dict[str, Optional[Union[Dict[str, Union[bool, str]], bool, str]]]
    ]: ...

class HiddenInput(Input):
    attrs: Dict[str, str]
    choices: django.forms.models.ModelChoiceIterator
    is_localized: bool
    is_required: bool
    input_type: str = ...
    template_name: str = ...

class MultipleHiddenInput(HiddenInput):
    attrs: Dict[str, str]
    choices: List[Tuple[str, str]]
    input_type: str
    is_required: bool
    template_name: str = ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[List[int], List[str]]],
        attrs: Optional[Dict[str, str]],
    ) -> Dict[
        str,
        Union[
            Dict[
                str,
                Union[
                    Dict[str, str],
                    List[Dict[str, Union[Dict[str, str], bool, str]]],
                    List[int],
                    bool,
                    str,
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[str, str],
                    List[Dict[str, Union[Dict[str, str], bool, str]]],
                    List[str],
                    bool,
                    str,
                ],
            ],
        ],
    ]: ...
    def value_from_datadict(
        self,
        data: Union[
            Dict[str, List[str]], Dict[str, Tuple[int, ...]], MultiValueDict
        ],
        files: Dict[Any, Any],
        name: str,
    ) -> Union[List[str], Tuple[int, ...]]: ...
    def format_value(
        self, value: Optional[Union[List[int], List[str]]]
    ) -> Union[List[int], List[str]]: ...

class FileInput(Input):
    attrs: Dict[str, Union[bool, str]]
    is_required: bool
    input_type: str = ...
    needs_multipart_form: bool = ...
    template_name: str = ...
    def format_value(self, value: Optional[str]) -> None: ...
    def value_from_datadict(
        self,
        data: Union[
            Dict[str, None], Dict[str, bool], Dict[str, str], QueryDict
        ],
        files: Dict[str, Union[SimpleUploadedFile, str]],
        name: str,
    ) -> Optional[Union[SimpleUploadedFile, str]]: ...
    def value_omitted_from_data(
        self,
        data: Dict[str, str],
        files: Dict[str, Union[SimpleUploadedFile, str]],
        name: str,
    ) -> bool: ...

class ClearableFileInput(FileInput):
    attrs: Dict[str, str]
    is_required: bool
    clear_checkbox_label: Any = ...
    initial_text: Any = ...
    input_text: Any = ...
    template_name: str = ...
    def clear_checkbox_name(self, name: str) -> str: ...
    def clear_checkbox_id(self, name: str) -> str: ...
    def is_initial(self, value: Optional[Union[File, str]]) -> bool: ...
    def format_value(
        self, value: Optional[Union[File, str]]
    ) -> Optional[FieldFile]: ...
    def get_context(self, name: Any, value: Any, attrs: Any): ...
    def value_from_datadict(
        self,
        data: Union[
            Dict[str, None], Dict[str, bool], Dict[str, str], QueryDict
        ],
        files: Dict[str, Union[SimpleUploadedFile, str]],
        name: str,
    ) -> Any: ...
    def use_required_attribute(
        self, initial: Optional[Union[FieldFile, str]]
    ) -> bool: ...
    def value_omitted_from_data(
        self,
        data: Dict[str, str],
        files: Dict[str, Union[SimpleUploadedFile, str]],
        name: str,
    ) -> bool: ...

class Textarea(Widget):
    attrs: Dict[str, Union[int, str]]
    is_required: bool
    template_name: str = ...
    def __init__(
        self, attrs: Optional[Union[Dict[str, int], Dict[str, str]]] = ...
    ) -> None: ...

class DateTimeBaseInput(TextInput):
    format_key: str = ...
    supports_microseconds: bool = ...
    format: Any = ...
    def __init__(
        self,
        attrs: Optional[Dict[str, Union[int, str]]] = ...,
        format: Optional[str] = ...,
    ) -> None: ...
    def format_value(
        self, value: Optional[Union[datetime, str]]
    ) -> Optional[str]: ...

class DateInput(DateTimeBaseInput):
    attrs: Dict[str, str]
    format: Optional[str]
    input_type: str
    is_localized: bool
    is_required: bool
    format_key: str = ...
    template_name: str = ...

class DateTimeInput(DateTimeBaseInput):
    attrs: Dict[Any, Any]
    format: Optional[str]
    input_type: str
    is_localized: bool
    is_required: bool
    format_key: str = ...
    template_name: str = ...

class TimeInput(DateTimeBaseInput):
    attrs: Dict[str, str]
    format: Optional[str]
    input_type: str
    is_localized: bool
    is_required: bool
    format_key: str = ...
    template_name: str = ...

class CheckboxInput(Input):
    attrs: Dict[str, str]
    is_required: bool
    input_type: str = ...
    template_name: str = ...
    check_test: Callable = ...
    def __init__(
        self,
        attrs: Optional[Dict[str, str]] = ...,
        check_test: Optional[Callable] = ...,
    ) -> None: ...
    def format_value(
        self, value: Optional[Union[int, str]]
    ) -> Optional[str]: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[int, str]],
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str, Dict[str, Optional[Union[Dict[str, Union[bool, str]], bool, str]]]
    ]: ...
    def value_from_datadict(
        self,
        data: Union[
            Dict[str, Optional[Union[List[int], datetime, int, str]]], QueryDict
        ],
        files: Union[Dict[str, SimpleUploadedFile], MultiValueDict],
        name: str,
    ) -> bool: ...
    def value_omitted_from_data(
        self,
        data: Union[
            Dict[str, Optional[Union[List[int], datetime, int, str]]], QueryDict
        ],
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> bool: ...

class ChoiceWidget(Widget):
    allow_multiple_selected: bool = ...
    input_type: Any = ...
    template_name: Any = ...
    option_template_name: Any = ...
    add_id_index: bool = ...
    checked_attribute: Any = ...
    option_inherits_attrs: bool = ...
    choices: Any = ...
    def __init__(
        self,
        attrs: Optional[Dict[str, Union[bool, str]]] = ...,
        choices: Union[
            Iterator[Any],
            List[List[Union[int, str]]],
            List[Tuple[Union[time, int], int]],
            List[int],
            Tuple,
        ] = ...,
    ) -> None: ...
    def __deepcopy__(self, memo: Dict[int, List[Any]]) -> ChoiceWidget: ...
    def subwidgets(
        self,
        name: str,
        value: Optional[List[str]],
        attrs: Dict[str, Union[bool, str]] = ...,
    ) -> None: ...
    def options(
        self,
        name: str,
        value: List[str],
        attrs: Dict[str, Union[bool, str]] = ...,
    ) -> None: ...
    def optgroups(
        self,
        name: str,
        value: List[str],
        attrs: Optional[Dict[str, Union[bool, str]]] = ...,
    ) -> List[
        Tuple[
            Optional[str],
            List[Dict[str, Union[Dict[str, Union[bool, str]], time, int, str]]],
            int,
        ]
    ]: ...
    def create_option(
        self,
        name: str,
        value: Union[time, int, str],
        label: Union[int, str],
        selected: Union[Set[str], bool],
        index: int,
        subindex: Optional[int] = ...,
        attrs: Optional[Dict[str, Union[bool, str]]] = ...,
    ) -> Dict[
        str,
        Union[
            Dict[str, Union[bool, str]],
            Dict[str, bool],
            Set[str],
            time,
            int,
            str,
        ],
    ]: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[List[int], List[str], Tuple[str, str], int, str]],
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str,
        Dict[
            str,
            Union[
                Dict[str, Union[bool, str]],
                List[
                    Tuple[
                        Optional[str],
                        Union[
                            List[Dict[str, Union[Dict[str, bool], bool, str]]],
                            List[Dict[str, Union[Dict[str, str], bool, str]]],
                        ],
                        int,
                    ]
                ],
                List[str],
                bool,
                str,
            ],
        ],
    ]: ...
    def id_for_label(self, id_: str, index: str = ...) -> str: ...
    def value_from_datadict(
        self,
        data: dict,
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> Optional[Union[List[str], int, str]]: ...
    def format_value(
        self,
        value: Optional[Union[List[int], List[str], Tuple[str, str], int, str]],
    ) -> List[str]: ...

class Select(ChoiceWidget):
    attrs: Dict[str, Union[bool, str]]
    choices: Union[
        List[List[Union[int, str]]],
        List[Tuple[datetime.time, Union[int, str]]],
        django.forms.fields.CallableChoiceIterator,
        django.forms.models.ModelChoiceIterator,
    ]
    is_required: bool
    input_type: str = ...
    template_name: str = ...
    option_template_name: str = ...
    add_id_index: bool = ...
    checked_attribute: Any = ...
    option_inherits_attrs: bool = ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[List[int], List[str], int, str]],
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str,
        Dict[
            str,
            Union[
                Dict[str, Union[bool, str]],
                List[
                    Tuple[
                        Optional[str],
                        List[
                            Dict[
                                str, Union[Dict[str, bool], Set[str], int, str]
                            ]
                        ],
                        int,
                    ]
                ],
                List[str],
                bool,
                str,
            ],
        ],
    ]: ...
    def use_required_attribute(self, initial: Any) -> bool: ...

class NullBooleanSelect(Select):
    attrs: Dict[Any, Any]
    def __init__(self, attrs: None = ...) -> None: ...
    def format_value(self, value: Optional[Union[bool, str]]) -> str: ...
    def value_from_datadict(
        self,
        data: Union[Dict[str, Union[bool, str]], QueryDict],
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> Optional[bool]: ...

class SelectMultiple(Select):
    attrs: Dict[Any, Any]
    choices: Union[
        List[Tuple[str, Union[Tuple[Tuple[str, str], Tuple[str, str]], str]]],
        django.forms.models.ModelChoiceIterator,
    ]
    is_required: bool
    allow_multiple_selected: bool = ...
    def value_from_datadict(
        self,
        data: Union[
            Dict[str, List[int]],
            Dict[str, Tuple[int, ...]],
            Dict[str, str],
            QueryDict,
        ],
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> Optional[Union[List[int], List[str], str]]: ...
    def value_omitted_from_data(
        self, data: Dict[str, str], files: Dict[Any, Any], name: str
    ) -> bool: ...

class RadioSelect(ChoiceWidget):
    attrs: Dict[str, str]
    choices: Union[
        List[
            Tuple[
                datetime.time,
                Union[Tuple[Tuple[str, str], Tuple[str, str]], str],
            ]
        ],
        List[int],
        django.forms.models.ModelChoiceIterator,
    ]
    is_required: bool
    input_type: str = ...
    template_name: str = ...
    option_template_name: str = ...

class CheckboxSelectMultiple(ChoiceWidget):
    attrs: Dict[str, str]
    choices: Union[
        List[
            Tuple[
                datetime.time,
                Union[Tuple[Tuple[str, str], Tuple[str, str]], str],
            ]
        ],
        django.forms.models.ModelChoiceIterator,
    ]
    is_required: bool
    allow_multiple_selected: bool = ...
    input_type: str = ...
    template_name: str = ...
    option_template_name: str = ...
    def use_required_attribute(self, initial: Optional[List[str]]) -> bool: ...
    def value_omitted_from_data(
        self, data: Dict[str, str], files: Dict[Any, Any], name: str
    ) -> bool: ...
    def id_for_label(self, id_: str, index: Optional[str] = ...) -> str: ...

class MultiWidget(Widget):
    attrs: Dict[Any, Any]
    template_name: str = ...
    widgets: List[django.forms.widgets.Widget] = ...
    def __init__(
        self,
        widgets: Union[
            List[Type[DateTimeBaseInput]], Tuple[Union[Type[TextInput], Input]]
        ],
        attrs: Optional[Dict[str, str]] = ...,
    ) -> None: ...
    @property
    def is_hidden(self) -> bool: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[List[datetime], datetime, str]],
        attrs: Optional[Dict[str, Union[bool, str]]],
    ) -> Dict[
        str,
        Union[
            Dict[
                str,
                Optional[
                    Union[
                        Dict[str, Union[bool, str]],
                        List[
                            Dict[
                                str,
                                Optional[
                                    Union[
                                        Dict[str, Union[bool, str]], bool, str
                                    ]
                                ],
                            ]
                        ],
                        bool,
                        str,
                    ]
                ],
            ],
            Dict[
                str,
                Union[
                    Dict[Any, Any],
                    List[
                        Dict[
                            str,
                            Union[
                                Dict[Any, Any],
                                List[
                                    Tuple[
                                        None,
                                        List[
                                            Dict[
                                                str,
                                                Union[
                                                    Dict[str, bool], bool, str
                                                ],
                                            ]
                                        ],
                                        int,
                                    ]
                                ],
                                List[str],
                                bool,
                                str,
                            ],
                        ]
                    ],
                    bool,
                    str,
                ],
            ],
        ],
    ]: ...
    def id_for_label(self, id_: str) -> str: ...
    def value_from_datadict(
        self,
        data: Union[Dict[str, Union[List[str], str]], QueryDict],
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> Union[List[None], List[str]]: ...
    def value_omitted_from_data(
        self,
        data: Union[Dict[str, str], QueryDict],
        files: Union[Dict[Any, Any], MultiValueDict],
        name: str,
    ) -> bool: ...
    def decompress(self, value: Any) -> None: ...
    media: Any = ...
    def __deepcopy__(
        self,
        memo: Dict[
            int,
            Union[
                List[Tuple[str, str]], List[Widget], OrderedDict, Field, Widget
            ],
        ],
    ) -> MultiWidget: ...
    @property
    def needs_multipart_form(self) -> bool: ...

class SplitDateTimeWidget(MultiWidget):
    attrs: Dict[Any, Any]
    is_required: bool
    widgets: List[django.forms.widgets.DateTimeBaseInput]
    supports_microseconds: bool = ...
    template_name: str = ...
    def __init__(
        self,
        attrs: Optional[Dict[str, str]] = ...,
        date_format: Optional[str] = ...,
        time_format: Optional[str] = ...,
        date_attrs: Optional[Dict[str, str]] = ...,
        time_attrs: Optional[Dict[str, str]] = ...,
    ) -> None: ...
    def decompress(
        self, value: Optional[Union[datetime, str]]
    ) -> Union[List[None], List[datetime]]: ...

class SplitHiddenDateTimeWidget(SplitDateTimeWidget):
    attrs: Dict[Any, Any]
    is_required: bool
    widgets: List[django.forms.widgets.DateTimeBaseInput]
    template_name: str = ...
    def __init__(
        self,
        attrs: Optional[Dict[str, str]] = ...,
        date_format: None = ...,
        time_format: None = ...,
        date_attrs: Optional[Dict[str, str]] = ...,
        time_attrs: Optional[Dict[str, str]] = ...,
    ) -> None: ...

class SelectDateWidget(Widget):
    none_value: Any = ...
    month_field: str = ...
    day_field: str = ...
    year_field: str = ...
    template_name: str = ...
    input_type: str = ...
    select_widget: Any = ...
    date_re: Any = ...
    attrs: Any = ...
    years: Any = ...
    months: Any = ...
    year_none_value: Any = ...
    month_none_value: Any = ...
    day_none_value: Any = ...
    def __init__(
        self,
        attrs: None = ...,
        years: Optional[Union[Tuple[Union[int, str]], range]] = ...,
        months: None = ...,
        empty_label: Optional[Union[Tuple[str, str], str]] = ...,
    ) -> None: ...
    def get_context(self, name: Any, value: Any, attrs: Any): ...
    def format_value(
        self, value: Optional[Union[date, str]]
    ) -> Dict[str, None]: ...
    def id_for_label(self, id_: str) -> str: ...
    def value_from_datadict(
        self, data: Dict[str, str], files: Dict[Any, Any], name: str
    ) -> Optional[str]: ...
    def value_omitted_from_data(
        self, data: Dict[str, str], files: Dict[Any, Any], name: str
    ) -> bool: ...
