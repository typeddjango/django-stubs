from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from django.db.models.expressions import Combinable
from django.db.models.fields import Field, _ErrorMessagesToOverride, _ValidatorCallable
from typing_extensions import Literal

from .mixins import CheckFieldDefaultMixin

_T = TypeVar("_T", bound=Optional[List[Any]])

class ArrayField(
    Generic[_T],
    CheckFieldDefaultMixin,
    Field[Union[_T, Combinable], _T],
):

    empty_strings_allowed: bool = ...
    default_error_messages: Any = ...
    base_field: Any = ...
    size: Any = ...
    default_validators: Any = ...
    from_db_value: Any = ...
    @overload
    def __init__(
        self: ArrayField[List[Any]],
        base_field: Field[Any, Any],
        size: Optional[int] = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Union[_T, Callable[[], _T]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Iterable[
            Union[Tuple[_T, str], Tuple[str, Iterable[Tuple[_T, str]]]]
        ] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: ArrayField[Optional[List[Any]]],
        base_field: Field[Any, Any],
        size: Optional[int] = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Optional[Union[_T, Callable[[], _T]]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Iterable[
            Union[Tuple[_T, str], Tuple[str, Iterable[Tuple[_T, str]]]]
        ] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[False] = ...,
        choices: None = ...,
        **kwargs: Any,
    ) -> ArrayField[List[Any]]: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[True],
        choices: None = ...,
        **kwargs: Any,
    ) -> ArrayField[Optional[List[Any]]]: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[False] = ...,
        choices: Iterable[Union[Tuple[_T, str], Tuple[str, Iterable[Tuple[_T, str]]]]],
        **kwargs: Any,
    ) -> ArrayField[_T]: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[True],
        choices: Iterable[Union[Tuple[_T, str], Tuple[str, Iterable[Tuple[_T, str]]]]],
        **kwargs: Any,
    ) -> ArrayField[Optional[_T]]: ...
    @property
    def description(self) -> str: ...  # type: ignore [override]
    def get_transform(self, name: Any) -> Any: ...
