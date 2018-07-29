from datetime import datetime
from django.template.base import (
    FilterExpression,
    NodeList,
    Parser,
    Token,
)
from django.template.context import Context
from django.utils.safestring import SafeText
from django.utils.timezone import FixedOffset
from typing import (
    Optional,
    Union,
)


def do_timezone(
    value: datetime,
    arg: FixedOffset
) -> datetimeobject: ...


def get_current_timezone_tag(
    parser: Parser,
    token: Token
) -> GetCurrentTimezoneNode: ...


def localtime(value: Optional[Union[str, datetime]]) -> Union[str, datetimeobject]: ...


def localtime_tag(
    parser: Parser,
    token: Token
) -> LocalTimeNode: ...


def timezone_tag(
    parser: Parser,
    token: Token
) -> TimezoneNode: ...


def utc(value: Optional[Union[str, datetime]]) -> Union[str, datetimeobject]: ...


class GetCurrentTimezoneNode:
    def __init__(self, variable: str) -> None: ...
    def render(self, context: Context) -> str: ...


class LocalTimeNode:
    def __init__(self, nodelist: NodeList, use_tz: bool) -> None: ...
    def render(self, context: Context) -> SafeText: ...


class TimezoneNode:
    def __init__(self, nodelist: NodeList, tz: FilterExpression) -> None: ...
    def render(self, context: Context) -> SafeText: ...