from collections.abc import Iterable, Iterator

from django.http import QueryDict
from django.http.request import _ImmutableQueryDict
from typing_extensions import assert_type

q = QueryDict("", False)
# Test constructor overloads -- Mutable
assert_type(QueryDict("querystring", True), QueryDict)
assert_type(QueryDict("querystring", mutable=True), QueryDict)

# Test constructor overloads -- Immutable
assert_type(QueryDict(), _ImmutableQueryDict)
assert_type(QueryDict("querystring"), _ImmutableQueryDict)
assert_type(QueryDict("querystring", False), _ImmutableQueryDict)
assert_type(QueryDict("querystring", mutable=False), _ImmutableQueryDict)


# Test ImmutableQueryDict
q = QueryDict()
assert_type(q["a"], str)
assert_type(q.get("a"), str | None)
assert_type(q.items(), Iterator[tuple[str, str | list[object]]])
assert_type(q.getlist("a"), list[str])
assert_type(q.lists(), Iterable[tuple[str, list[str]]])

# Test MutableQueryDict
mut_q = QueryDict(mutable=True)
mut_q["a"] = "3"
mut_q["a"] = ["1", "2"]  # type: ignore[assignment]  # pyright: ignore[reportArgumentType]

assert_type(mut_q.pop("a"), list[str])
assert_type(mut_q.pop("a", 12), list[str] | int)
assert_type(mut_q.popitem(), tuple[str, list[str]])
