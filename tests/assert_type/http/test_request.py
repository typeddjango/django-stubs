from collections.abc import Iterable, Iterator
from typing import assert_type

from django.http import QueryDict

# Test ImmutableQueryDict
q = QueryDict("a=1&a=2&a=3")
assert_type(q["a"], str)
assert_type(q.get("a"), str | None)
assert_type(q.items(), Iterator[tuple[str, str | list[object]]])
assert_type(q.getlist("a"), list[str])
assert_type(q.lists(), Iterable[tuple[str, list[str]]])

# Test MutableQueryDict
mut_q = QueryDict("a=1&a=2&a=3", mutable=True)
mut_q["a"] = "3"
mut_q["a"] = ["1", "2"]  # type: ignore[assignment]

assert_type(mut_q.pop("a"), list[str])
assert_type(mut_q.pop("a", 12), list[str] | int)
assert_type(mut_q.popitem(), tuple[str, list[str]])
