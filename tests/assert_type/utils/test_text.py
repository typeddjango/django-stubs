from django.utils.functional import _StrPromise
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy
from typing_extensions import assert_type

result = format_lazy("{}", "test")
assert_type(result, _StrPromise)

result_lazy_fmt = format_lazy(gettext_lazy("Hello {}"), "world")
assert_type(result_lazy_fmt, _StrPromise)

result_multi = format_lazy("{} {} {}", "a", "b", "c")
assert_type(result_multi, _StrPromise)

result_kwargs = format_lazy("{name}: {value}", name="key", value=42)
assert_type(result_kwargs, _StrPromise)
