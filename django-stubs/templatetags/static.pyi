from django.template.base import (
    FilterExpression,
    Parser,
    Token,
)
from django.template.context import Context
from typing import Optional


def do_static(
    parser: Parser,
    token: Token
) -> StaticNode: ...


def get_media_prefix(
    parser: Parser,
    token: Token
) -> PrefixNode: ...


def get_static_prefix(
    parser: Parser,
    token: Token
) -> PrefixNode: ...


def static(path: str) -> str: ...


class PrefixNode:
    def __init__(self, varname: None = ..., name: str = ...) -> None: ...
    @classmethod
    def handle_simple(cls, name: str) -> str: ...
    @classmethod
    def handle_token(
        cls,
        parser: Parser,
        token: Token,
        name: str
    ) -> PrefixNode: ...
    def render(self, context: Context) -> str: ...


class StaticNode:
    def __init__(
        self,
        varname: Optional[str] = ...,
        path: FilterExpression = ...
    ) -> None: ...
    @classmethod
    def handle_simple(cls, path: str) -> str: ...
    @classmethod
    def handle_token(
        cls,
        parser: Parser,
        token: Token
    ) -> StaticNode: ...
    def render(self, context: Context) -> str: ...
    def url(self, context: Context) -> str: ...