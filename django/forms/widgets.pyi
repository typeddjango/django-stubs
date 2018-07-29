from datetime import (
    date,
    datetime,
    time,
)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.forms.renderers import DjangoTemplates
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import SafeText
from itertools import chain
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)


class CheckboxInput:
    def __init__(self, attrs: Optional[Dict[str, str]] = ..., check_test: Optional[Callable] = ...) -> None: ...
    def format_value(self, value: Optional[Union[str, int]]) -> Optional[str]: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[str, int]],
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...
    def value_from_datadict(
        self,
        data: Any,
        files: Union[Dict[str, SimpleUploadedFile], MultiValueDict],
        name: str
    ) -> bool: ...
    def value_omitted_from_data(
        self,
        data: Union[Dict[str, str], Dict[str, Union[str, List[int]]], Dict[str, Union[int, str, None, datetime]], QueryDict],
        files: MultiValueDict,
        name: str
    ) -> bool: ...


class CheckboxSelectMultiple:
    def id_for_label(self, id_: str, index: Optional[str] = ...) -> str: ...
    def use_required_attribute(self, initial: None) -> bool: ...
    def value_omitted_from_data(self, data: Dict[Any, Any], files: Dict[Any, Any], name: str) -> bool: ...


class ChoiceWidget:
    def __deepcopy__(self, memo: Dict[int, Any]) -> ChoiceWidget: ...
    def __init__(
        self,
        attrs: Optional[Union[Dict[str, Union[bool, str]], Dict[str, str]]] = ...,
        choices: Any = ...
    ) -> None: ...
    def create_option(
        self,
        name: str,
        value: Union[str, time, int],
        label: Union[str, int],
        selected: Union[bool, Set[str]],
        index: int,
        subindex: Optional[int] = ...,
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]] = ...
    ) -> Dict[str, Any]: ...
    def format_value(self, value: Any) -> List[str]: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...
    def id_for_label(self, id_: str, index: str = ...) -> str: ...
    def optgroups(
        self,
        name: str,
        value: List[str],
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]] = ...
    ) -> Any: ...
    def options(self, name: str, value: List[str], attrs: Dict[str, Union[bool, str]] = ...) -> None: ...
    def subwidgets(self, name: str, value: Optional[List[str]], attrs: Dict[str, Union[bool, str]] = ...) -> None: ...
    def value_from_datadict(
        self,
        data: Any,
        files: MultiValueDict,
        name: str
    ) -> Optional[Union[str, int, List[str]]]: ...


class ClearableFileInput:
    def clear_checkbox_id(self, name: str) -> str: ...
    def clear_checkbox_name(self, name: str) -> str: ...
    def format_value(
        self,
        value: Optional[Union[str, FieldFile]]
    ) -> Optional[FieldFile]: ...
    def is_initial(self, value: Any) -> bool: ...
    def use_required_attribute(self, initial: Optional[FieldFile]) -> bool: ...
    def value_from_datadict(
        self,
        data: Union[Dict[str, bool], Dict[str, str], Dict[str, None], QueryDict],
        files: Dict[str, Union[str, SimpleUploadedFile]],
        name: str
    ) -> Optional[Union[str, SimpleUploadedFile]]: ...
    def value_omitted_from_data(self, data: Dict[str, str], files: Dict[Any, Any], name: str) -> bool: ...


class DateTimeBaseInput:
    def __init__(self, attrs: Optional[Dict[str, str]] = ..., format: Optional[str] = ...) -> None: ...
    def format_value(self, value: Optional[Union[time, str, date]]) -> Optional[str]: ...


class FileInput:
    def format_value(self, value: None) -> None: ...
    def value_from_datadict(
        self,
        data: Union[Dict[str, bool], Dict[str, str], QueryDict],
        files: Dict[str, SimpleUploadedFile],
        name: str
    ) -> Optional[SimpleUploadedFile]: ...
    def value_omitted_from_data(
        self,
        data: Dict[Any, Any],
        files: Dict[str, Union[str, SimpleUploadedFile]],
        name: str
    ) -> bool: ...


class Input:
    def __init__(self, attrs: Optional[Union[Dict[str, str], Dict[str, bool], Dict[str, int]]] = ...) -> None: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...


class Media:
    def __add__(self, other: Media) -> Media: ...
    def __getitem__(self, name: str) -> Media: ...
    def __init__(
        self,
        media: Optional[Type[object]] = ...,
        css: Optional[Union[Dict[str, Tuple[str, str]], Dict[str, Tuple[str]], Dict[str, List[str]]]] = ...,
        js: Any = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    def absolute_path(self, path: str) -> str: ...
    @staticmethod
    def merge(list_1: Union[List[str], Tuple[str], List[int]], list_2: Any) -> Union[List[int], List[str]]: ...
    def render(self) -> SafeText: ...
    def render_css(self) -> chain: ...
    def render_js(self) -> List[SafeText]: ...


class MediaDefiningClass:
    @staticmethod
    def __new__(mcs: Type[MediaDefiningClass], name: str, bases: Tuple, attrs: Any) -> Any: ...


class MultiWidget:
    def __deepcopy__(self, memo: Dict[int, Any]) -> MultiWidget: ...
    def __init__(self, widgets: Any, attrs: Optional[Dict[str, str]] = ...) -> None: ...
    def _get_media(self) -> Media: ...
    def get_context(
        self,
        name: str,
        value: Optional[Union[str, datetime, List[str]]],
        attrs: Optional[Union[Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...
    def id_for_label(self, id_: str) -> str: ...
    @property
    def is_hidden(self) -> bool: ...
    @property
    def needs_multipart_form(self) -> bool: ...
    def value_from_datadict(
        self,
        data: Union[Dict[str, str], Dict[str, Union[str, List[str]]], QueryDict],
        files: MultiValueDict,
        name: str
    ) -> Union[List[None], List[str]]: ...
    def value_omitted_from_data(
        self,
        data: Union[Dict[str, str], QueryDict],
        files: MultiValueDict,
        name: str
    ) -> bool: ...


class MultipleHiddenInput:
    def format_value(self, value: Union[List[int], List[str]]) -> Union[List[int], List[str]]: ...
    def get_context(self, name: str, value: List[str], attrs: Optional[Dict[str, str]]) -> Dict[str, Dict[str, Any]]: ...
    def value_from_datadict(
        self,
        data: MultiValueDict,
        files: Dict[Any, Any],
        name: str
    ) -> List[str]: ...


class NullBooleanSelect:
    def __init__(self, attrs: None = ...) -> None: ...
    def format_value(self, value: Optional[str]) -> str: ...
    def value_from_datadict(self, data: Dict[str, Union[bool, str]], files: Dict[Any, Any], name: str) -> Optional[bool]: ...


class PasswordInput:
    def __init__(self, attrs: Optional[Dict[str, bool]] = ..., render_value: bool = ...) -> None: ...
    def get_context(
        self,
        name: str,
        value: Optional[str],
        attrs: Optional[Union[Dict[str, Union[bool, str]], Dict[str, bool]]]
    ) -> Dict[str, Dict[str, Any]]: ...


class Select:
    @staticmethod
    def _choice_has_empty_value(choice: Union[Tuple[None, str], Tuple[str, str]]) -> bool: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...
    def use_required_attribute(self, initial: Any) -> bool: ...


class SelectDateWidget:
    def __init__(
        self,
        attrs: None = ...,
        years: Optional[Union[range, Tuple[str]]] = ...,
        months: None = ...,
        empty_label: Optional[Tuple[str, str, str]] = ...
    ) -> None: ...
    @staticmethod
    def _parse_date_fmt() -> Iterator[str]: ...
    def format_value(self, value: Optional[Union[str, date]]) -> Dict[str, Union[None, int, str]]: ...
    def value_from_datadict(self, data: Dict[str, str], files: Dict[Any, Any], name: str) -> Optional[str]: ...
    def value_omitted_from_data(self, data: Dict[str, str], files: Dict[Any, Any], name: str) -> bool: ...


class SelectMultiple:
    def value_from_datadict(
        self,
        data: Any,
        files: MultiValueDict,
        name: str
    ) -> Optional[Union[str, List[int], List[str]]]: ...
    def value_omitted_from_data(self, data: Dict[Any, Any], files: Dict[Any, Any], name: str) -> bool: ...


class SplitDateTimeWidget:
    def __init__(
        self,
        attrs: Optional[Dict[str, str]] = ...,
        date_format: None = ...,
        time_format: None = ...,
        date_attrs: Optional[Dict[str, str]] = ...,
        time_attrs: Optional[Dict[str, str]] = ...
    ) -> None: ...
    def decompress(
        self,
        value: Optional[datetime]
    ) -> Union[List[None], List[Union[date, time]]]: ...


class SplitHiddenDateTimeWidget:
    def __init__(
        self,
        attrs: None = ...,
        date_format: None = ...,
        time_format: None = ...,
        date_attrs: None = ...,
        time_attrs: None = ...
    ) -> None: ...


class Textarea:
    def __init__(self, attrs: Optional[Union[Dict[str, str], Dict[str, int]]] = ...) -> None: ...


class Widget:
    def __deepcopy__(self, memo: Dict[int, Any]) -> Widget: ...
    def __init__(self, attrs: Any = ...) -> None: ...
    def _render(
        self,
        template_name: str,
        context: Dict[str, Any],
        renderer: Optional[DjangoTemplates] = ...
    ) -> SafeText: ...
    def build_attrs(
        self,
        base_attrs: Dict[str, Union[str, int, float]],
        extra_attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]] = ...
    ) -> Dict[str, Union[str, int, float]]: ...
    def format_value(self, value: Any) -> Optional[str]: ...
    def get_context(
        self,
        name: str,
        value: Any,
        attrs: Optional[Union[Dict[str, bool], Dict[str, Union[bool, str]], Dict[str, str]]]
    ) -> Dict[str, Any]: ...