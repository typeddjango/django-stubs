from typing import Any

from django.utils.encoding import force_bytes, force_str, smart_bytes, smart_str
from typing_extensions import assert_type


def test_any_input() -> None:
    x: Any = None
    assert_type(force_bytes(x), bytes)
    assert_type(force_str(x), str)
    assert_type(smart_bytes(x), bytes)
    assert_type(smart_str(x), str)
