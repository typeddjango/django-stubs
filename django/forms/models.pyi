from collections import OrderedDict
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.forms.fields import Field
from django.forms.utils import ErrorList
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)
from uuid import UUID


def _get_foreign_key(
    parent_model: Any,
    model: Any,
    fk_name: Optional[str] = ...,
    can_fail: bool = ...
) -> ForeignKey: ...


def apply_limit_choices_to_to_formfield(formfield: Field) -> None: ...


class BaseModelForm:
    def __init__(
        self,
        data: Any = ...,
        files: Optional[Dict[str, SimpleUploadedFile]] = ...,
        auto_id: Union[str, bool] = ...,
        prefix: None = ...,
        initial: Optional[Dict[str, Union[Model, List[Model], QuerySet]]] = ...,
        error_class: Type[ErrorList] = ...,
        label_suffix: None = ...,
        empty_permitted: bool = ...,
        instance: Any = ...,
        use_required_attribute: None = ...,
        renderer: None = ...
    ) -> None: ...
    def _get_validation_exclusions(self) -> List[str]: ...
    def _post_clean(self) -> None: ...
    def _save_m2m(self) -> None: ...
    def _update_errors(self, errors: ValidationError) -> None: ...
    def clean(self) -> Dict[str, Any]: ...
    def save(self, commit: bool = ...) -> Model: ...
    def validate_unique(self) -> None: ...


class InlineForeignKeyField:
    def __init__(
        self,
        parent_instance: Model,
        *args,
        pk_field = ...,
        to_field = ...,
        **kwargs
    ) -> None: ...
    def clean(self, value: Optional[Union[str, int]]) -> Model: ...
    def has_changed(self, initial: Optional[Union[str, int]], data: Optional[Union[str, int]]) -> bool: ...


class ModelChoiceField:
    def __deepcopy__(self, memo: Dict[int, Any]) -> ModelChoiceField: ...
    def __init__(
        self,
        queryset: QuerySet,
        *,
        empty_label = ...,
        required = ...,
        widget = ...,
        label = ...,
        initial = ...,
        help_text = ...,
        to_field_name = ...,
        limit_choices_to = ...,
        **kwargs
    ) -> None: ...
    def _get_choices(self) -> ModelChoiceIterator: ...
    def _get_queryset(self) -> QuerySet: ...
    def _set_queryset(self, queryset: Union[QuerySet, Manager]) -> None: ...
    def get_limit_choices_to(self) -> Any: ...
    def has_changed(self, initial: Optional[Union[int, UUID]], data: Optional[Union[str, int]]) -> bool: ...
    def label_from_instance(self, obj: Model) -> str: ...
    def prepare_value(self, value: Any) -> Optional[Union[UUID, str, int]]: ...
    def to_python(self, value: Optional[Union[str, List[List[str]], int]]) -> Any: ...
    def validate(self, value: Any) -> None: ...


class ModelChoiceIterator:
    def __bool__(self) -> bool: ...
    def __init__(self, field: ModelChoiceField) -> None: ...
    def __iter__(self) -> Iterator[Union[Tuple[int, str], Tuple[str, str]]]: ...
    def __len__(self) -> int: ...
    def choice(self, obj: Model) -> Tuple[int, str]: ...


class ModelFormMetaclass:
    @staticmethod
    def __new__(
        mcs: Type[ModelFormMetaclass],
        name: str,
        bases: Tuple[Type[ModelForm]],
        attrs: OrderedDict
    ) -> Any: ...


class ModelFormOptions:
    def __init__(self, options: Any = ...) -> None: ...


class ModelMultipleChoiceField:
    def __init__(self, queryset: QuerySet, **kwargs) -> None: ...
    def _check_values(
        self,
        value: Union[List[int], Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], List[str]]
    ) -> QuerySet: ...
    def clean(self, value: Union[List[List[str]], str, List[int], List[str]]) -> QuerySet: ...
    def has_changed(self, initial: List[Model], data: List[str]) -> bool: ...
    def prepare_value(self, value: Any) -> Any: ...
    def to_python(
        self,
        value: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    ) -> List[Model]: ...