from datetime import (
    date,
    time,
    timedelta,
)
from decimal import Decimal
from django.utils.safestring import SafeText
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def _property_resolver(arg: Union[str, int]) -> Callable: ...


def add(
    value: Union[date, Tuple[int, int], str, int],
    arg: Union[SafeText, Tuple[int, int], timedelta, int]
) -> Union[str, Tuple[int, int, int, int], date, int]: ...


def addslashes(value: str) -> str: ...


def capfirst(value: str) -> str: ...


def center(value: str, arg: SafeText) -> str: ...


def cut(value: str, arg: str) -> str: ...


def date(value: Optional[Union[time, date, str]], arg: Optional[str] = ...) -> str: ...


def default(value: Optional[Union[int, str]], arg: Union[SafeText, int]) -> Union[int, str]: ...


def default_if_none(value: Optional[str], arg: Union[str, int]) -> Union[str, int]: ...


def dictsort(
    value: Union[List[Dict[str, Union[str, int]]], List[Dict[str, str]], List[Tuple[str, str]]],
    arg: Union[str, int]
) -> Union[List[Dict[str, Union[str, int]]], List[Dict[str, str]], List[Tuple[str, str]]]: ...


def dictsortreversed(value: str, arg: str) -> str: ...


def divisibleby(value: int, arg: int) -> bool: ...


def escape_filter(value: str) -> SafeText: ...


def escapejs_filter(value: str) -> SafeText: ...


def filesizeformat(bytes_: Union[str, int]) -> str: ...


def first(value: Union[str, List[str]]) -> str: ...


def floatformat(text: Optional[Union[Decimal, str, float]], arg: Union[str, int] = ...) -> str: ...


def force_escape(value: str) -> SafeText: ...


def get_digit(value: int, arg: int) -> int: ...


def iriencode(value: str) -> str: ...


def join(value: object, arg: str, autoescape: bool = ...) -> object: ...


def json_script(value: Dict[str, str], element_id: SafeText) -> SafeText: ...


def last(value: List[str]) -> str: ...


def length(value: Any) -> int: ...


def length_is(value: Any, arg: Union[SafeText, int]) -> Union[bool, str]: ...


def linebreaks_filter(value: str, autoescape: bool = ...) -> SafeText: ...


def linebreaksbr(value: str, autoescape: bool = ...) -> SafeText: ...


def linenumbers(value: str, autoescape: bool = ...) -> SafeText: ...


def ljust(value: str, arg: Union[SafeText, int]) -> str: ...


def lower(value: str) -> str: ...


def make_list(value: str) -> List[str]: ...


def phone2numeric_filter(value: str) -> str: ...


def pluralize(value: object, arg: str = ...) -> str: ...


def pprint(value: object) -> str: ...


def random(value: Union[List[str], List[SafeText]]) -> str: ...


def rjust(value: str, arg: Union[SafeText, int]) -> str: ...


def safe(value: str) -> SafeText: ...


def safeseq(value: List[str]) -> List[SafeText]: ...


def slice_filter(value: str, arg: str) -> str: ...


def slugify(value: str) -> SafeText: ...


def stringformat(value: object, arg: str) -> str: ...


def striptags(value: str) -> str: ...


def time(value: Optional[Union[time, str, date]], arg: Optional[str] = ...) -> str: ...


def timesince_filter(value: Optional[date], arg: Optional[date] = ...) -> str: ...


def timeuntil_filter(value: date, arg: Optional[date] = ...) -> str: ...


def title(value: str) -> str: ...


def truncatechars(value: str, arg: Union[SafeText, int]) -> str: ...


def truncatechars_html(value: str, arg: Union[str, int]) -> str: ...


def truncatewords(value: str, arg: Union[SafeText, int]) -> str: ...


def truncatewords_html(value: str, arg: int) -> str: ...


def unordered_list(value: Any, autoescape: bool = ...) -> SafeText: ...


def upper(value: str) -> str: ...


def urlencode(value: str, safe: None = ...) -> str: ...


def urlize(value: str, autoescape: bool = ...) -> SafeText: ...


def urlizetrunc(
    value: str,
    limit: Union[SafeText, int],
    autoescape: bool = ...
) -> SafeText: ...


def wordcount(value: str) -> int: ...


def wordwrap(value: str, arg: Union[SafeText, int]) -> str: ...


def yesno(value: Optional[int], arg: Optional[str] = ...) -> Optional[str]: ...