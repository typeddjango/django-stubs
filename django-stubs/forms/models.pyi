from collections import OrderedDict
from datetime import date
from functools import partial
from typing import (Any, Callable, Dict, Iterator, List, Optional, Tuple, Type,
                    Union)

from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import Permission
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.forms.fields import CharField, ChoiceField, Field, URLField
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.forms.formsets import BaseFormSet
from django.forms.utils import ErrorList
from django.forms.widgets import Textarea, TextInput, Widget
from django.http.request import QueryDict
from django.utils.datastructures import MultiValueDict

ALL_FIELDS: str

def model_to_dict(
    instance: Model,
    fields: Optional[Union[List[Union[str, Callable]], Tuple[str]]] = ...,
    exclude: Optional[List[Union[str, Callable]]] = ...,
) -> Dict[str, Optional[Union[int, date, str, List[Any]]]]: ...
def fields_for_model(
    model: Type[Model],
    fields: Optional[Union[List[Union[str, Callable]], Tuple]] = ...,
    exclude: Optional[List[Union[str, Callable]]] = ...,
    widgets: Optional[Dict[str, Union[Type[Textarea], TextInput]]] = ...,
    formfield_callback: Optional[partial] = ...,
    localized_fields: None = ...,
    labels: Optional[Dict[str, str]] = ...,
    help_texts: Optional[Dict[str, str]] = ...,
    error_messages: Optional[Dict[str, Dict[str, str]]] = ...,
    field_classes: Optional[
        Dict[str, Type[Union[URLField, UsernameField]]]
    ] = ...,
    *,
    apply_limit_choices_to: bool = ...
) -> OrderedDict: ...

class ModelFormOptions:
    model: Optional[Type[django.db.models.base.Model]] = ...
    fields: Optional[Union[List[Union[str, Callable]], Tuple, str]] = ...
    exclude: Optional[Union[List[Union[str, Callable]], Tuple, str]] = ...
    widgets: Optional[
        Union[
            Dict[
                str,
                Type[
                    Union[
                        django.forms.widgets.TextInput,
                        django.forms.widgets.HiddenInput,
                    ]
                ],
            ],
            Dict[
                str,
                Union[
                    Type[django.forms.widgets.Textarea],
                    django.forms.widgets.Widget,
                ],
            ],
        ]
    ] = ...
    localized_fields: Optional[Union[str, Tuple[str]]] = ...
    labels: Optional[Dict[str, str]] = ...
    help_texts: Optional[Dict[str, str]] = ...
    error_messages: Optional[Dict[str, Dict[str, str]]] = ...
    field_classes: Optional[
        Dict[
            str,
            Type[
                Union[
                    django.forms.fields.URLField,
                    django.contrib.auth.forms.UsernameField,
                    django.forms.fields.SlugField,
                ]
            ],
        ]
    ] = ...
    def __init__(self, options: Type[Any] = ...) -> None: ...

class ModelFormMetaclass(DeclarativeFieldsMetaclass):
    def __new__(
        mcs: Type[ModelFormMetaclass],
        name: str,
        bases: Tuple[Type[ModelForm]],
        attrs: OrderedDict,
    ) -> Type[ModelForm]: ...

class BaseModelForm(BaseForm):
    instance: Any = ...
    def __init__(
        self,
        data: Optional[Union[Dict[str, str], QueryDict]] = ...,
        files: Optional[MultiValueDict] = ...,
        auto_id: str = ...,
        prefix: None = ...,
        initial: Optional[Dict[Any, Any]] = ...,
        error_class: Type[ErrorList] = ...,
        label_suffix: None = ...,
        empty_permitted: bool = ...,
        instance: Optional[Model] = ...,
        use_required_attribute: None = ...,
        renderer: None = ...,
    ) -> None: ...
    def clean(self) -> Dict[str, Union[int, date]]: ...
    def validate_unique(self) -> None: ...
    save_m2m: Any = ...
    def save(self, commit: bool = ...) -> Model: ...

class ModelForm(BaseModelForm): ...

def modelform_factory(
    model: Any,
    form: Any = ...,
    fields: Optional[Any] = ...,
    exclude: Optional[Any] = ...,
    formfield_callback: Optional[Any] = ...,
    widgets: Optional[Any] = ...,
    localized_fields: Optional[Any] = ...,
    labels: Optional[Any] = ...,
    help_texts: Optional[Any] = ...,
    error_messages: Optional[Any] = ...,
    field_classes: Optional[Any] = ...,
): ...

class BaseModelFormSet(BaseFormSet):
    model: Any = ...
    unique_fields: Any = ...
    queryset: Any = ...
    initial_extra: Any = ...
    def __init__(
        self,
        data: Optional[Any] = ...,
        files: Optional[Any] = ...,
        auto_id: str = ...,
        prefix: Optional[Any] = ...,
        queryset: Optional[Any] = ...,
        *,
        initial: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def initial_form_count(self): ...
    def get_queryset(self): ...
    def save_new(self, form: Any, commit: bool = ...): ...
    def save_existing(self, form: Any, instance: Any, commit: bool = ...): ...
    def delete_existing(self, obj: Any, commit: bool = ...) -> None: ...
    saved_forms: Any = ...
    save_m2m: Any = ...
    def save(self, commit: bool = ...): ...
    def clean(self) -> None: ...
    def validate_unique(self) -> None: ...
    def get_unique_error_message(self, unique_check: Any): ...
    def get_date_error_message(self, date_check: Any): ...
    def get_form_error(self): ...
    changed_objects: Any = ...
    deleted_objects: Any = ...
    def save_existing_objects(self, commit: bool = ...): ...
    new_objects: Any = ...
    def save_new_objects(self, commit: bool = ...): ...
    def add_fields(self, form: Any, index: Any): ...

def modelformset_factory(
    model: Any,
    form: Any = ...,
    formfield_callback: Optional[Any] = ...,
    formset: Any = ...,
    extra: int = ...,
    can_delete: bool = ...,
    can_order: bool = ...,
    max_num: Optional[Any] = ...,
    fields: Optional[Any] = ...,
    exclude: Optional[Any] = ...,
    widgets: Optional[Any] = ...,
    validate_max: bool = ...,
    localized_fields: Optional[Any] = ...,
    labels: Optional[Any] = ...,
    help_texts: Optional[Any] = ...,
    error_messages: Optional[Any] = ...,
    min_num: Optional[Any] = ...,
    validate_min: bool = ...,
    field_classes: Optional[Any] = ...,
): ...

class BaseInlineFormSet(BaseModelFormSet):
    instance: Any = ...
    save_as_new: Any = ...
    unique_fields: Any = ...
    def __init__(
        self,
        data: Optional[Any] = ...,
        files: Optional[Any] = ...,
        instance: Optional[Any] = ...,
        save_as_new: bool = ...,
        prefix: Optional[Any] = ...,
        queryset: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def initial_form_count(self): ...
    @classmethod
    def get_default_prefix(cls): ...
    def save_new(self, form: Any, commit: bool = ...): ...
    def add_fields(self, form: Any, index: Any) -> None: ...
    def get_unique_error_message(self, unique_check: Any): ...

def inlineformset_factory(
    parent_model: Any,
    model: Any,
    form: Any = ...,
    formset: Any = ...,
    fk_name: Optional[Any] = ...,
    fields: Optional[Any] = ...,
    exclude: Optional[Any] = ...,
    extra: int = ...,
    can_order: bool = ...,
    can_delete: bool = ...,
    max_num: Optional[Any] = ...,
    formfield_callback: Optional[Any] = ...,
    widgets: Optional[Any] = ...,
    validate_max: bool = ...,
    localized_fields: Optional[Any] = ...,
    labels: Optional[Any] = ...,
    help_texts: Optional[Any] = ...,
    error_messages: Optional[Any] = ...,
    min_num: Optional[Any] = ...,
    validate_min: bool = ...,
    field_classes: Optional[Any] = ...,
): ...

class InlineForeignKeyField(Field):
    disabled: bool
    help_text: str
    initial: Optional[Union[str, django.db.models.base.Model, int]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    widget: Any = ...
    default_error_messages: Any = ...
    parent_instance: django.db.models.base.Model = ...
    pk_field: bool = ...
    to_field: Optional[str] = ...
    def __init__(
        self,
        parent_instance: Model,
        *args: Any,
        pk_field: bool = ...,
        to_field: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def clean(self, value: Optional[str]) -> Model: ...
    def has_changed(self, initial: int, data: str) -> bool: ...

class ModelChoiceIterator:
    field: django.forms.models.ModelChoiceField = ...
    queryset: Optional[django.db.models.query.QuerySet] = ...
    def __init__(self, field: Any) -> None: ...
    def __iter__(self) -> Iterator[Tuple[str, str]]: ...
    def __len__(self): ...
    def __bool__(self): ...
    def choice(self, obj: Model) -> Tuple[int, str]: ...

class ModelChoiceField(ChoiceField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    initial: Optional[Union[Callable, uuid.UUID, int, str]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    widget: django.forms.widgets.Select
    default_error_messages: Any = ...
    iterator: Any = ...
    empty_label: Optional[str] = ...
    queryset: Any = ...
    limit_choices_to: None = ...
    to_field_name: None = ...
    def __init__(
        self,
        queryset: Any,
        *,
        empty_label: str = ...,
        required: bool = ...,
        widget: Optional[Any] = ...,
        label: Optional[Any] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        to_field_name: Optional[Any] = ...,
        limit_choices_to: Optional[Any] = ...,
        **kwargs: Any
    ) -> None: ...
    def get_limit_choices_to(self) -> Dict[Any, Any]: ...
    def __deepcopy__(
        self,
        memo: Dict[
            int,
            Union[
                OrderedDict,
                Widget,
                List[Union[Widget, Field]],
                Field,
                List[Union[AdminTextInputWidget, CharField]],
            ],
        ],
    ) -> ModelChoiceField: ...
    def label_from_instance(self, obj: Model) -> str: ...
    choices: Any = ...
    def prepare_value(
        self, value: Optional[Union[int, str, Model]]
    ) -> Optional[Union[str, int]]: ...
    def to_python(self, value: str) -> Optional[Model]: ...
    def validate(self, value: Model) -> None: ...
    def has_changed(self, initial: None, data: str) -> bool: ...

class ModelMultipleChoiceField(ModelChoiceField):
    disabled: bool
    empty_label: None
    help_text: str
    initial: Optional[Union[Callable, List[int]]]
    label: Optional[str]
    label_suffix: None
    localize: bool
    required: bool
    show_hidden_initial: bool
    widget: Any = ...
    hidden_widget: Any = ...
    default_error_messages: Any = ...
    def __init__(self, queryset: Any, **kwargs: Any) -> None: ...
    def to_python(self, value: Any): ...
    def clean(self, value: List[str]) -> QuerySet: ...
    def prepare_value(
        self, value: Union[Permission, List[str]]
    ) -> Union[List[str], int]: ...
    def has_changed(self, initial: List[Any], data: List[str]) -> bool: ...
