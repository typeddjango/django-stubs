from django.utils.safestring import SafeString, mark_safe
from typing_extensions import assert_type

s = "hello"
assert_type(mark_safe(s), SafeString)
assert_type(mark_safe(s) + mark_safe(s), SafeString)
assert_type(s + mark_safe(s), str)

s += mark_safe(s)
assert_type(s, str)

ms = mark_safe(s)
ms += mark_safe(s)
assert_type(ms, SafeString)


# mark_safe as decorator preserves function type
@mark_safe
def func(s: str) -> str:
    return s


assert_type(func("test"), str)
