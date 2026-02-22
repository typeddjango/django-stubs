from typing import Any

from django.utils.encoding import force_bytes, force_str, smart_bytes, smart_str
from typing_extensions import assert_type


def test_any_input() -> None:
    x: Any = None
    assert_type(force_bytes(x), bytes)
    assert_type(force_str(x), str)
    assert_type(smart_bytes(x), bytes)
    assert_type(smart_str(x), str)


class S(str):
    pass


def test_force_bytes() -> None:
    assert_type(force_bytes(123), bytes)
    assert_type(force_bytes(123, strings_only=True), int)


def test_force_str() -> None:
    assert_type(force_str(123), str)
    assert_type(force_str(123, strings_only=True), int)
    assert_type(force_str("foo"), str)
    assert_type(force_str("foo", strings_only=True), str)
    assert_type(force_str(S("foo"), strings_only=True), S)


def test_smart_bytes() -> None:
    assert_type(smart_bytes(123), bytes)
    assert_type(smart_bytes(123, strings_only=True), int)


def test_smart_str() -> None:
    assert_type(smart_str(123), str)
    assert_type(smart_str(123, strings_only=True), int)
    assert_type(smart_str("foo"), str)
    assert_type(smart_str("foo", strings_only=True), str)
    assert_type(smart_str(S("foo"), strings_only=True), S)
