from django.utils.safestring import SafeText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def _strip_once(value: str) -> str: ...


def avoid_wrapping(value: str) -> str: ...


def conditional_escape(text: Any) -> str: ...


def escape(text: Any) -> SafeText: ...


def escapejs(value: str) -> SafeText: ...


def format_html(format_string: str, *args, **kwargs) -> SafeText: ...


def format_html_join(
    sep: str,
    format_string: str,
    args_generator: Union[List[Tuple[str]], List[Tuple[str, str]]]
) -> SafeText: ...


def json_script(value: Dict[str, str], element_id: SafeText) -> SafeText: ...


def linebreaks(value: str, autoescape: bool = ...) -> str: ...


def smart_urlquote(url: str) -> str: ...


def strip_spaces_between_tags(value: str) -> str: ...


def strip_tags(value: str) -> str: ...


def urlize(
    text: str,
    trim_url_limit: Optional[int] = ...,
    nofollow: bool = ...,
    autoescape: bool = ...
) -> str: ...


class MLStripper:
    def __init__(self) -> None: ...
    def get_data(self) -> str: ...
    def handle_charref(self, name: str) -> None: ...
    def handle_data(self, d: str) -> None: ...
    def handle_entityref(self, name: str) -> None: ...