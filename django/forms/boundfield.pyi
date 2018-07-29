from django.forms.fields import Field
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.forms.renderers import DjangoTemplates
from django.forms.utils import ErrorList
from django.forms.widgets import (
    ChoiceWidget,
    HiddenInput,
    SplitHiddenDateTimeWidget,
    Widget,
)
from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


class BoundField:
    def __getitem__(
        self,
        idx: Union[slice, str, int]
    ) -> Union[List[BoundWidget], BoundWidget]: ...
    def __init__(
        self,
        form: Union[Form, ModelForm],
        field: Field,
        name: str
    ) -> None: ...
    def __len__(self) -> int: ...
    def as_hidden(self, attrs: None = ..., **kwargs) -> SafeText: ...
    def as_text(self, attrs: None = ..., **kwargs) -> SafeText: ...
    def as_textarea(self, attrs: None = ..., **kwargs) -> SafeText: ...
    def as_widget(
        self,
        widget: Optional[Union[HiddenInput, SplitHiddenDateTimeWidget]] = ...,
        attrs: None = ...,
        only_initial: bool = ...
    ) -> SafeText: ...
    @property
    def auto_id(self) -> str: ...
    def build_widget_attrs(
        self,
        attrs: Dict[str, str],
        widget: Optional[Widget] = ...
    ) -> Dict[str, Union[bool, str]]: ...
    def css_classes(self, extra_classes: None = ...) -> str: ...
    @property
    def data(self) -> Any: ...
    @property
    def errors(self) -> ErrorList: ...
    @cached_property
    def initial(self) -> Any: ...
    @property
    def is_hidden(self) -> bool: ...
    def label_tag(
        self,
        contents: Optional[SafeText] = ...,
        attrs: Optional[Dict[str, str]] = ...,
        label_suffix: Optional[str] = ...
    ) -> SafeText: ...
    @cached_property
    def subwidgets(self) -> List[BoundWidget]: ...
    def value(self) -> Any: ...


class BoundWidget:
    def __init__(
        self,
        parent_widget: ChoiceWidget,
        data: Dict[str, Any],
        renderer: DjangoTemplates
    ) -> None: ...
    @property
    def choice_label(self) -> str: ...
    def tag(self, wrap_label: bool = ...) -> SafeText: ...
    @property
    def template_name(self) -> str: ...