from datetime import date, time
from decimal import Decimal
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.base import Message
from django.core.exceptions import FieldDoesNotExist
from django.db.models.base import Model
from django.db.models.fields.files import FieldFile
from django.db.models.query import QuerySet
from django.forms.boundfield import BoundField, BoundWidget
from django.forms.forms import BaseForm
from django.forms.utils import ErrorDict
from django.forms.widgets import Media
from django.urls.resolvers import CheckURLMixin, LocalePrefixPattern

ISO_INPUT_FORMATS: Any
FORMAT_SETTINGS: Any

def reset_format_cache() -> None: ...
def iter_format_modules(
    lang: str, format_module_path: Optional[Union[List[str], str]] = ...
) -> Iterator[Any]: ...
def get_format_modules(
    lang: Optional[str] = ..., reverse: bool = ...
) -> List[Any]: ...
def get_format(
    format_type: str, lang: Optional[str] = ..., use_l10n: Optional[bool] = ...
) -> Union[List[str], int, str]: ...

get_format_lazy: Any

def date_format(
    value: Union[date, time, str],
    format: Optional[str] = ...,
    use_l10n: Optional[bool] = ...,
) -> str: ...
def time_format(
    value: Union[date, time, str],
    format: Optional[str] = ...,
    use_l10n: None = ...,
) -> str: ...
def number_format(
    value: Union[Decimal, float, int, str],
    decimal_pos: Optional[int] = ...,
    use_l10n: Optional[bool] = ...,
    force_grouping: bool = ...,
) -> str: ...
def localize(
    value: Optional[
        Union[
            AttributeError,
            Dict[str, str],
            KeyError,
            List[ErrorDict],
            List[int],
            List[str],
            Tuple[int, int, int, int],
            TypeError,
            date,
            Decimal,
            AnonymousUser,
            Message,
            FieldDoesNotExist,
            Model,
            FieldFile,
            QuerySet,
            BoundField,
            BoundWidget,
            BaseForm,
            Media,
            CheckURLMixin,
            LocalePrefixPattern,
            float,
            int,
            str,
        ]
    ],
    use_l10n: Optional[bool] = ...,
) -> Optional[
    Union[
        AttributeError,
        Dict[str, str],
        KeyError,
        List[ErrorDict],
        List[int],
        List[str],
        Tuple[int, int, int, int],
        TypeError,
        AnonymousUser,
        Message,
        FieldDoesNotExist,
        Model,
        FieldFile,
        QuerySet,
        BoundField,
        BoundWidget,
        BaseForm,
        Media,
        CheckURLMixin,
        LocalePrefixPattern,
        str,
    ]
]: ...
def localize_input(
    value: Optional[Union[date, time, Decimal, float, int, str]],
    default: Optional[str] = ...,
) -> Optional[str]: ...
def sanitize_separators(
    value: Union[Decimal, int, str]
) -> Union[Decimal, int, str]: ...
