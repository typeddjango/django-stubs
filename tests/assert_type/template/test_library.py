from __future__ import annotations

import datetime
from typing import Any

from django import template
from django.template.base import Parser, Token, TokenType
from django.template.defaulttags import CycleNode
from typing_extensions import assert_type

register = template.Library()


# register.filter (bare)
@register.filter
def lower(value: str) -> str:
    return value.lower()


assert_type(lower("test"), str)


# register.filter (named)
@register.filter(name="tolower")
def lower2(value: str) -> str:
    return value.lower()


assert_type(lower2("test"), str)


# register.filter with all flags
@register.filter(name="plain", is_safe=True, needs_autoescape=False, expects_localtime=False)
def plain_filter(value: str) -> str:
    return value


assert_type(plain_filter("x"), str)


# Negative: non-bool values for flag kwargs are rejected
register.filter("bad_is_safe", is_safe="yes")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
register.filter("bad_needs_autoescape", needs_autoescape="no")  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]
register.filter("bad_expects_localtime", expects_localtime=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]

# Negative: unknown kwargs are rejected
register.filter("unknown_flag", safe=True)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]  # pyrefly: ignore[no-matching-overload]  # ty: ignore[no-matching-overload]


# register.simple_tag (bare)
@register.simple_tag
def current_time(format_string: str) -> str:
    return datetime.datetime.now().strftime(format_string)


assert_type(current_time("%H"), str)


# register.simple_tag with takes_context
@register.simple_tag(takes_context=True)
def current_time_ctx(context: dict[str, Any], format_string: str) -> str:
    return "test"


assert_type(current_time_ctx({}, "%H"), str)


# register.simple_tag (named)
@register.simple_tag(name="minustwo")
def some_function(value: int) -> int:
    return value - 2


assert_type(some_function(5), int)


# register.simple_tag via call
def f(s: str) -> str:
    return s * 2


assert_type(register.simple_tag(f, name="double")("x"), str)


# register.simple_block_tag
assert_type(register.simple_block_tag(f, name="double")("x"), str)


@register.simple_block_tag
def block_tag_bare(format_string: str) -> str:
    return datetime.datetime.now().strftime(format_string)


assert_type(block_tag_bare("%H"), str)


@register.simple_block_tag(name="minustwo")
def block_tag_named(value: int) -> int:
    return value - 2


assert_type(block_tag_named(5), int)


# register.tag (bare)
@register.tag
def cycle(parser: Parser, token: Token) -> CycleNode:
    return CycleNode([])


assert_type(cycle(Parser([]), Token(token_type=TokenType.TEXT, contents="")), CycleNode)


# register.tag (named)
@register.tag(name="cycle")
def cycle_impl(parser: Parser, token: Token) -> CycleNode:
    return CycleNode([])


assert_type(cycle_impl(Parser([]), Token(token_type=TokenType.TEXT, contents="")), CycleNode)


# register.inclusion_tag
@register.inclusion_tag("results.html")
def format_results(results: list[str]) -> str:
    return ", ".join(results)


assert_type(format_results(["a", "b"]), str)


# register.inclusion_tag with takes_context
@register.inclusion_tag("results.html", takes_context=True)
def format_results_ctx(context: dict[str, Any], results: list[str]) -> str:
    return ", ".join(results)


assert_type(format_results_ctx({}, ["a", "b"]), str)


# register.inclusion_tag via call
def format_results_func(results: list[str]) -> str:
    return ", ".join(results)


assert_type(register.inclusion_tag("results.html", format_results_func)(["a"]), str)
