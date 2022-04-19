import sys
from typing import (
    Any,
    Callable,
    ClassVar,
    Collection,
    Container,
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from uuid import UUID

from django.db import models
from django.db.models import ForeignKey
from django.db.models.base import Model
from django.db.models.fields import _AllLimitChoicesTo, _ChoicesCallable, _FieldChoices, _LimitChoicesTo
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.forms.fields import CallableChoiceIterator, ChoiceField, Field, _ClassLevelWidgetT
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.forms.formsets import BaseFormSet
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList, _DataT, _FilesT
from django.forms.widgets import ChoiceWidget, Input, Widget
from django.utils.datastructures import _IndexableCollection, _ListOrTuple, _PropertyDescriptor

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

ALL_FIELDS: Literal["__all__"]

_Fields = Union[_ListOrTuple[str], Literal["__all__"]]
_Widgets = Dict[str, Union[Type[Widget], Widget]]
_Labels = Dict[str, str]
_HelpTexts = Dict[str, str]
_ErrorMessages = Dict[str, Dict[str, str]]
_FormFieldCallback = Callable[[models.Field], Field]

_M = TypeVar("_M", bound=Model)
_ParentM = TypeVar("_ParentM", bound=Model)

def construct_instance(
    form: BaseForm, instance: _M, fields: Optional[Container[str]] = ..., exclude: Optional[Container[str]] = ...
) -> _M: ...
def model_to_dict(
    instance: Model, fields: Optional[_Fields] = ..., exclude: Optional[_Fields] = ...
) -> Dict[str, Any]: ...
def apply_limit_choices_to_to_formfield(formfield: Field) -> None: ...
def fields_for_model(
    model: Type[Model],
    fields: Optional[_Fields] = ...,
    exclude: Optional[_Fields] = ...,
    widgets: Optional[_Widgets] = ...,
    formfield_callback: Optional[_FormFieldCallback] = ...,
    localized_fields: Optional[_Fields] = ...,
    labels: Optional[_Labels] = ...,
    help_texts: Optional[_HelpTexts] = ...,
    error_messages: Optional[_ErrorMessages] = ...,
    field_classes: Optional[Mapping[str, Type[Field]]] = ...,
    *,
    apply_limit_choices_to: bool = ...,
) -> Dict[str, Any]: ...

class ModelFormOptions(Generic[_M]):
    model: Type[_M] = ...
    fields: Optional[_Fields] = ...
    exclude: Optional[_Fields] = ...
    widgets: Optional[_Widgets] = ...
    localized_fields: Optional[_Fields] = ...
    labels: Optional[_Labels] = ...
    help_texts: Optional[_HelpTexts] = ...
    error_messages: Optional[_ErrorMessages] = ...
    field_classes: Optional[Dict[str, Type[Field]]] = ...
    def __init__(self, options: Optional[type] = ...) -> None: ...

class ModelFormMetaclass(DeclarativeFieldsMetaclass): ...

class BaseModelForm(Generic[_M], BaseForm):
    instance: _M
    _meta: ModelFormOptions[_M]
    def __init__(
        self,
        data: Optional[_DataT] = ...,
        files: Optional[_FilesT] = ...,
        auto_id: Union[bool, str] = ...,
        prefix: Optional[str] = ...,
        initial: Optional[Mapping[str, Any]] = ...,
        error_class: Type[ErrorList] = ...,
        label_suffix: Optional[str] = ...,
        empty_permitted: bool = ...,
        instance: Optional[_M] = ...,
        use_required_attribute: Optional[bool] = ...,
        renderer: BaseRenderer = ...,
    ) -> None: ...
    def validate_unique(self) -> None: ...
    def save(self, commit: bool = ...) -> _M: ...
    def save_m2m(self) -> None: ...

class ModelForm(BaseModelForm[_M], metaclass=ModelFormMetaclass):
    base_fields: ClassVar[Dict[str, Field]] = ...

def modelform_factory(
    model: Type[_M],
    form: Type[ModelForm[_M]] = ...,
    fields: Optional[_Fields] = ...,
    exclude: Optional[_Fields] = ...,
    formfield_callback: Optional[_FormFieldCallback] = ...,
    widgets: Optional[_Widgets] = ...,
    localized_fields: Optional[_Fields] = ...,
    labels: Optional[_Labels] = ...,
    help_texts: Optional[_HelpTexts] = ...,
    error_messages: Optional[_ErrorMessages] = ...,
    field_classes: Optional[Mapping[str, Type[Field]]] = ...,
) -> Type[ModelForm[_M]]: ...

_ModelFormT = TypeVar("_ModelFormT", bound=ModelForm)

class BaseModelFormSet(Generic[_M, _ModelFormT], BaseFormSet[_ModelFormT]):
    model: Type[_M] = ...
    unique_fields: Collection[str] = ...
    queryset: Optional[QuerySet[_M]] = ...
    initial_extra: Optional[Sequence[Dict[str, Any]]] = ...
    def __init__(
        self,
        data: Optional[_DataT] = ...,
        files: Optional[_FilesT] = ...,
        auto_id: str = ...,
        prefix: Optional[str] = ...,
        queryset: Optional[QuerySet[_M]] = ...,
        *,
        initial: Optional[Sequence[Dict[str, Any]]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def initial_form_count(self) -> int: ...
    def get_queryset(self) -> _IndexableCollection[_M]: ...
    def save_new(self, form: _ModelFormT, commit: bool = ...) -> _M: ...
    def save_existing(self, form: _ModelFormT, instance: _M, commit: bool = ...) -> _M: ...
    def delete_existing(self, obj: _M, commit: bool = ...) -> None: ...
    saved_forms: List[_ModelFormT] = ...
    save_m2m: Callable[[], None] = ...
    def save(self, commit: bool = ...) -> List[_M]: ...
    def clean(self) -> None: ...
    def validate_unique(self) -> None: ...
    def get_unique_error_message(self, unique_check: Sequence[str]) -> str: ...
    def get_date_error_message(self, date_check: Tuple[str, Literal["date", "year", "month"], str, str]) -> str: ...
    def get_form_error(self) -> str: ...
    changed_objects: List[Tuple[_M, List[str]]] = ...
    deleted_objects: List[_M] = ...
    def save_existing_objects(self, commit: bool = ...) -> List[_M]: ...
    new_objects: List[_M] = ...
    def save_new_objects(self, commit: bool = ...) -> List[_M]: ...
    def add_fields(self, form: _ModelFormT, index: Optional[int]) -> None: ...

def modelformset_factory(
    model: Type[_M],
    form: Type[_ModelFormT] = ...,
    formfield_callback: Optional[_FormFieldCallback] = ...,
    formset: Type[BaseModelFormSet] = ...,
    extra: int = ...,
    can_delete: bool = ...,
    can_order: bool = ...,
    max_num: Optional[int] = ...,
    fields: Optional[_Fields] = ...,
    exclude: Optional[_Fields] = ...,
    widgets: Optional[_Widgets] = ...,
    validate_max: bool = ...,
    localized_fields: Optional[_Fields] = ...,
    labels: Optional[_Labels] = ...,
    help_texts: Optional[_HelpTexts] = ...,
    error_messages: Optional[_ErrorMessages] = ...,
    min_num: Optional[int] = ...,
    validate_min: bool = ...,
    field_classes: Optional[Mapping[str, Type[Field]]] = ...,
    absolute_max: Optional[int] = ...,
    can_delete_extra: bool = ...,
) -> Type[BaseModelFormSet[_M, _ModelFormT]]: ...

class BaseInlineFormSet(Generic[_M, _ParentM, _ModelFormT], BaseModelFormSet[_M, _ModelFormT]):
    instance: _ParentM
    save_as_new: bool = ...
    unique_fields: Collection[str] = ...
    fk: ForeignKey  # set by inlineformset_set
    def __init__(
        self,
        data: Optional[_DataT] = ...,
        files: Optional[_FilesT] = ...,
        instance: Optional[_ParentM] = ...,
        save_as_new: bool = ...,
        prefix: Optional[str] = ...,
        queryset: Optional[QuerySet[_M]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def initial_form_count(self) -> int: ...
    @classmethod
    def get_default_prefix(cls) -> str: ...
    def save_new(self, form: _ModelFormT, commit: bool = ...) -> _M: ...
    def add_fields(self, form: _ModelFormT, index: Optional[int]) -> None: ...
    def get_unique_error_message(self, unique_check: Sequence[str]) -> str: ...

def inlineformset_factory(
    parent_model: Type[_ParentM],
    model: Type[_M],
    form: Type[_ModelFormT] = ...,
    formset: Type[BaseInlineFormSet] = ...,
    fk_name: Optional[str] = ...,
    fields: Optional[_Fields] = ...,
    exclude: Optional[_Fields] = ...,
    extra: int = ...,
    can_order: bool = ...,
    can_delete: bool = ...,
    max_num: Optional[int] = ...,
    formfield_callback: Optional[_FormFieldCallback] = ...,
    widgets: Optional[_Widgets] = ...,
    validate_max: bool = ...,
    localized_fields: Optional[Sequence[str]] = ...,
    labels: Optional[_Labels] = ...,
    help_texts: Optional[_HelpTexts] = ...,
    error_messages: Optional[_ErrorMessages] = ...,
    min_num: Optional[int] = ...,
    validate_min: bool = ...,
    field_classes: Optional[Mapping[str, Type[Field]]] = ...,
    absolute_max: Optional[int] = ...,
    can_delete_extra: bool = ...,
) -> Type[BaseInlineFormSet[_M, _ParentM, _ModelFormT]]: ...

class InlineForeignKeyField(Field):
    disabled: bool
    help_text: str
    required: bool
    show_hidden_initial: bool
    widget: _ClassLevelWidgetT = ...
    default_error_messages: Dict[str, str] = ...
    parent_instance: Model = ...
    pk_field: bool = ...
    to_field: Optional[str] = ...
    def __init__(
        self,
        parent_instance: Model,
        *args: Any,
        pk_field: bool = ...,
        to_field: Optional[str] = ...,
        **kwargs: Any,
    ) -> None: ...
    def clean(self, value: Any) -> Model: ...
    def has_changed(self, initial: Any, data: Any) -> bool: ...

class ModelChoiceIteratorValue:
    def __init__(self, value: Any, instance: Model) -> None: ...
    def __str__(self) -> str: ...

class ModelChoiceIterator:
    field: ModelChoiceField = ...
    queryset: QuerySet = ...
    def __init__(self, field: ModelChoiceField) -> None: ...
    def __iter__(self) -> Iterator[Tuple[Union[ModelChoiceIteratorValue, str], str]]: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def choice(self, obj: Model) -> Tuple[ModelChoiceIteratorValue, str]: ...

class ModelChoiceField(ChoiceField):
    disabled: bool
    error_messages: Dict[str, str]
    help_text: str
    required: bool
    show_hidden_initial: bool
    validators: List[Any]
    default_error_messages: Dict[str, str] = ...
    iterator: Type[ModelChoiceIterator] = ...
    empty_label: Optional[str] = ...
    queryset: Optional[QuerySet[models.Model]] = ...
    limit_choices_to: Optional[_AllLimitChoicesTo] = ...
    to_field_name: Optional[str] = ...
    def __init__(
        self,
        queryset: Union[None, Manager[models.Model], QuerySet[models.Model]],
        *,
        empty_label: Optional[str] = ...,
        required: bool = ...,
        widget: Optional[Union[Widget, Type[Widget]]] = ...,
        label: Optional[str] = ...,
        initial: Optional[Any] = ...,
        help_text: str = ...,
        to_field_name: Optional[str] = ...,
        limit_choices_to: Optional[_AllLimitChoicesTo] = ...,
        blank: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    def get_limit_choices_to(self) -> _LimitChoicesTo: ...
    def label_from_instance(self, obj: Model) -> str: ...
    choices: _PropertyDescriptor[
        Union[_FieldChoices, _ChoicesCallable, CallableChoiceIterator],
        Union[_FieldChoices, CallableChoiceIterator, ModelChoiceIterator],
    ] = ...
    def prepare_value(self, value: Any) -> Any: ...
    def to_python(self, value: Optional[Any]) -> Optional[Model]: ...
    def validate(self, value: Optional[Model]) -> None: ...
    def has_changed(self, initial: Optional[Union[Model, int, str, UUID]], data: Optional[Union[int, str]]) -> bool: ...

class ModelMultipleChoiceField(ModelChoiceField):
    disabled: bool
    empty_label: Optional[str]
    help_text: str
    required: bool
    show_hidden_initial: bool
    widget: _ClassLevelWidgetT = ...
    hidden_widget: Type[Widget] = ...
    default_error_messages: Dict[str, str] = ...
    def __init__(self, queryset: Union[None, Manager[Model], QuerySet[Model]], **kwargs: Any) -> None: ...
    def to_python(self, value: Any) -> List[Model]: ...  # type: ignore[override]
    def clean(self, value: Any) -> QuerySet[Model]: ...
    def prepare_value(self, value: Any) -> Any: ...
    def has_changed(self, initial: Optional[Collection[Any]], data: Optional[Collection[Any]]) -> bool: ...  # type: ignore

def modelform_defines_fields(form_class: Type[ModelForm]) -> bool: ...
@overload
def _get_foreign_key(  # type: ignore
    parent_model: Type[Model], model: Type[Model], fk_name: Optional[str] = ..., can_fail: Literal[True] = ...
) -> Optional[ForeignKey]: ...
@overload
def _get_foreign_key(
    parent_model: Type[Model], model: Type[Model], fk_name: Optional[str] = ..., can_fail: Literal[False] = ...
) -> ForeignKey: ...
