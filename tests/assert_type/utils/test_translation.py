from __future__ import annotations

from django.utils.functional import _StrPromise
from django.utils.translation import ngettext, ngettext_lazy, npgettext, npgettext_lazy
from typing_extensions import assert_type

# ngettext / npgettext accept int and float
assert_type(ngettext("apple", "apples", 1), str)
assert_type(ngettext("apple", "apples", 1.0), str)
assert_type(npgettext("fruit", "apple", "apples", 1), str)
assert_type(npgettext("fruit", "apple", "apples", 1.0), str)

# lazy variants also accept str and None (deferred number resolution)
assert_type(ngettext_lazy("apple", "apples", 1), _StrPromise)
assert_type(ngettext_lazy("apple", "apples", "count"), _StrPromise)
assert_type(ngettext_lazy("apple", "apples"), _StrPromise)
assert_type(npgettext_lazy("fruit", "apple", "apples", 1), _StrPromise)
assert_type(npgettext_lazy("fruit", "apple", "apples", "count"), _StrPromise)
assert_type(npgettext_lazy("fruit", "apple", "apples"), _StrPromise)
