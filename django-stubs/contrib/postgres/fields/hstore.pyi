from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from django.db.models import Field, Transform
from typing_extensions import Literal

from .mixins import CheckFieldDefaultMixin

_Choice = Tuple[Any, Any]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]
_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

_T = TypeVar("_T")

class HStoreField(Generic[_T], CheckFieldDefaultMixin, Field[Any, Any]):
    @overload
    def __init__(
        self: HStoreField[Dict[str, Optional[str]]],
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    @overload
    def __init__(
        self: HStoreField[Optional[Dict[str, Optional[str]]]],
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    def get_transform(self, name) -> Any: ...
    def __get__(self: HStoreField[_T], instance: Any, owner: Any) -> _T: ...
    def __set__(self: HStoreField[_T], instance: Any, value: _T) -> None: ...

class KeyTransform(Transform):
    def __init__(self, key_name: str, *args: Any, **kwargs: Any): ...

class KeyTransformFactory:
    def __init__(self, key_name: str): ...
    def __call__(self, *args, **kwargs) -> KeyTransform: ...

class KeysTransform(Transform): ...
class ValuesTransform(Transform): ...
