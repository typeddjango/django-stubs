from typing import Any, Dict, Optional, Sequence, Type, Union

from django import forms as forms
from django.contrib.postgres.validators import ArrayMaxLengthValidator as ArrayMaxLengthValidator
from django.contrib.postgres.validators import ArrayMinLengthValidator as ArrayMinLengthValidator
from django.core.exceptions import ValidationError as ValidationError
from django.db.models.fields import _ErrorMessagesT
from django.forms.fields import _ClassLevelWidgetT
from django.forms.utils import _DataT, _FilesT
from django.forms.widgets import Media, _OptAttrs

from ..utils import prefix_validation_error as prefix_validation_error

class SimpleArrayField(forms.CharField):
    default_error_messages: _ErrorMessagesT = ...
    base_field: Type[forms.Field]
    delimiter: str
    min_length: Optional[int]
    max_length: Optional[int]
    def __init__(
        self,
        base_field: Type[forms.Field],
        *,
        delimiter: str = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        **kwargs: Any
    ) -> None: ...
    def clean(self, value: Any) -> Sequence[Any]: ...
    def prepare_value(self, value: Any) -> Any: ...
    def to_python(self, value: Any) -> Sequence[Any]: ...  # type: ignore
    def validate(self, value: Sequence[Any]) -> None: ...
    def run_validators(self, value: Sequence[Any]) -> None: ...
    def has_changed(self, initial: Any, data: Any) -> bool: ...

class SplitArrayWidget(forms.Widget):
    template_name: str
    widget: _ClassLevelWidgetT
    size: int
    def __init__(self, widget: Union[forms.Widget, Type[forms.Widget]], size: int, **kwargs: Any) -> None: ...
    @property
    def is_hidden(self) -> bool: ...
    def value_from_datadict(self, data: _DataT, files: _FilesT, name: str) -> Any: ...
    def value_omitted_from_data(self, data: _DataT, files: _FilesT, name: str) -> bool: ...
    def id_for_label(self, id_: str) -> str: ...
    def get_context(self, name: str, value: Any, attrs: Optional[_OptAttrs] = ...) -> Dict[str, Any]: ...
    @property
    def media(self) -> Media: ...  # type: ignore
    @property
    def needs_multipart_form(self) -> bool: ...  # type: ignore

class SplitArrayField(forms.Field):
    default_error_messages: _ErrorMessagesT = ...
    base_field: Type[forms.Field]
    size: int
    remove_trailing_nulls: bool
    def __init__(
        self, base_field: Type[forms.Field], size: int, *, remove_trailing_nulls: bool = ..., **kwargs: Any
    ) -> None: ...
    def to_python(self, value: Any) -> Sequence[Any]: ...
    def clean(self, value: Any) -> Sequence[Any]: ...
    def has_changed(self, initial: Any, data: Any) -> bool: ...
