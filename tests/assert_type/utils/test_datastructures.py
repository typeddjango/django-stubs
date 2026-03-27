from django.utils.datastructures import MultiValueDict
from typing_extensions import assert_type

# Constructors
var1: MultiValueDict[str, str] = MultiValueDict()
d2: dict[str, list[str | int]] = {"foo": ["Foo"], "bar": [2, 3]}
var2 = MultiValueDict(d2)
d3: tuple[tuple[str, list[str | int]], ...] = (("foo", ["Foo"]), ("bar", [2, 3]))
var3: MultiValueDict[str, str | int] = MultiValueDict(d3)

assert_type(var1, MultiValueDict[str, str])
assert_type(var2, MultiValueDict[str, str | int])
assert_type(var3, MultiValueDict[str, str | int])

# __getitem__, get, getlist
d = MultiValueDict({"foo": ["Foo"]})
d.setlist("bar", [])
assert_type(d["foo"], str | list[object])
assert_type(d["bar"], str | list[object])
assert_type(d.get("bar"), str | None)
assert_type(d.get("bar", 1), str | int)  # ty: ignore[type-assertion-failure]
assert_type(d.getlist("bar"), list[str])  # ty: ignore[type-assertion-failure]
assert_type(d.getlist("bar", [1]), list[str] | list[int])
assert_type(d.getlist("baz", True), list[str] | bool)  # ty: ignore[type-assertion-failure]

# setters
assert_type(d.setlistdefault("baz"), list[str])
d.setlistdefault("baz", [1])  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
assert_type(d.setlistdefault("baz", []), list[str])
d.appendlist("baz", "Baz")
d.appendlist("baz", 1)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

# iterators
assert_type(list(d.items()), list[tuple[str, str | list[object]]])
assert_type(list(d.keys()), list[str])
assert_type(list(d.values()), list[str | list[object]])
assert_type(d.dict(), dict[str, str | list[object]])  # ty: ignore[type-assertion-failure]
