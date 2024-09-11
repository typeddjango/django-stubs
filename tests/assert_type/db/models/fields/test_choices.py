from collections.abc import Callable, Mapping, Sequence
from typing import Tuple, TypeVar

from django.db import models
from typing_extensions import assert_type

_T = TypeVar("_T")


def to_named_seq(func: Callable[[], _T]) -> Callable[[], Sequence[Tuple[str, _T]]]:
    def inner() -> Sequence[Tuple[str, _T]]:
        return [("title", func())]

    return inner


def to_named_mapping(func: Callable[[], _T]) -> Callable[[], Mapping[str, _T]]:
    def inner() -> Mapping[str, _T]:
        return {"title": func()}

    return inner


def str_tuple() -> Sequence[Tuple[str, str]]:
    return (("foo", "bar"), ("fuzz", "bazz"))


def str_mapping() -> Mapping[str, str]:
    return {"foo": "bar", "fuzz": "bazz"}


def int_tuple() -> Sequence[Tuple[int, str]]:
    return ((1, "bar"), (2, "bazz"))


def int_mapping() -> Mapping[int, str]:
    return {3: "bar", 4: "bazz"}


class TestModel(models.Model):
    class TextChoices(models.TextChoices):
        FIRST = "foo", "bar"
        SECOND = "foo2", "bar"

    class IntegerChoices(models.IntegerChoices):
        FIRST = 1, "bar"
        SECOND = 2, "bar"

    char1 = models.CharField[str, str](max_length=5, choices=TextChoices, default="foo")
    char2 = models.CharField[str, str](max_length=5, choices=str_tuple, default="foo")
    char3 = models.CharField[str, str](max_length=5, choices=str_mapping, default="foo")
    char4 = models.CharField[str, str](max_length=5, choices=str_tuple(), default="foo")
    char5 = models.CharField[str, str](max_length=5, choices=str_mapping(), default="foo")
    char6 = models.CharField[str, str](max_length=5, choices=to_named_seq(str_tuple), default="foo")
    char7 = models.CharField[str, str](max_length=5, choices=to_named_mapping(str_mapping), default="foo")
    char8 = models.CharField[str, str](max_length=5, choices=to_named_seq(str_tuple)(), default="foo")
    char9 = models.CharField[str, str](max_length=5, choices=to_named_mapping(str_mapping)(), default="foo")

    int1 = models.IntegerField[int, int](choices=IntegerChoices, default=1)
    int2 = models.IntegerField[int, int](choices=int_tuple, default=1)
    int3 = models.IntegerField[int, int](choices=int_mapping, default=1)
    int4 = models.IntegerField[int, int](choices=int_tuple(), default=1)
    int5 = models.IntegerField[int, int](choices=int_mapping(), default=1)
    int6 = models.IntegerField[int, int](choices=to_named_seq(int_tuple), default=1)
    int7 = models.IntegerField[int, int](choices=to_named_seq(int_mapping), default=1)
    int8 = models.IntegerField[int, int](choices=to_named_seq(int_tuple)(), default=1)
    int9 = models.IntegerField[int, int](choices=to_named_seq(int_mapping)(), default=1)


instance = TestModel()
assert_type(instance.char1, str)
assert_type(instance.char2, str)
assert_type(instance.char3, str)
assert_type(instance.char4, str)
assert_type(instance.char5, str)
assert_type(instance.char6, str)
assert_type(instance.char7, str)
assert_type(instance.char8, str)
assert_type(instance.char9, str)

assert_type(instance.int1, int)
assert_type(instance.int2, int)
assert_type(instance.int3, int)
assert_type(instance.int4, int)
assert_type(instance.int5, int)
assert_type(instance.int6, int)
assert_type(instance.int7, int)
assert_type(instance.int8, int)
assert_type(instance.int9, int)
