from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.db import models
from typing_extensions import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

_T = TypeVar("_T")


def to_named_seq(func: Callable[[], _T]) -> Callable[[], Sequence[tuple[str, _T]]]:
    def inner() -> Sequence[tuple[str, _T]]:
        return [("title", func())]

    return inner


def to_named_mapping(func: Callable[[], _T]) -> Callable[[], Mapping[str, _T]]:
    def inner() -> Mapping[str, _T]:
        return {"title": func()}

    return inner


def str_tuple() -> Sequence[tuple[str, str]]:
    return (("foo", "bar"), ("fuzz", "bazz"))


def str_mapping() -> Mapping[str, str]:
    return {"foo": "bar", "fuzz": "bazz"}


def int_tuple() -> Sequence[tuple[int, str]]:
    return ((1, "bar"), (2, "bazz"))


def int_mapping() -> Mapping[int, str]:
    return {3: "bar", 4: "bazz"}


# Invalid choices
class BadForm(forms.Form):
    my_choice = forms.ChoiceField(choices="test")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]


# Valid choices
class TestForm(forms.Form):
    class TextChoices(models.TextChoices):
        FIRST = "foo", "bar"
        SECOND = "foo2", "bar"

    class IntegerChoices(models.IntegerChoices):
        FIRST = 1, "bar"
        SECOND = 2, "bar"

    char1 = forms.ChoiceField(choices=TextChoices)
    char2 = forms.ChoiceField(choices=str_tuple)
    char3 = forms.ChoiceField(choices=str_mapping)
    char4 = forms.ChoiceField(choices=str_tuple())
    char5 = forms.ChoiceField(choices=str_mapping())
    char6 = forms.ChoiceField(choices=to_named_seq(str_tuple))
    char7 = forms.ChoiceField(choices=to_named_mapping(str_mapping))
    char8 = forms.ChoiceField(choices=to_named_seq(str_tuple)())
    char9 = forms.ChoiceField(choices=to_named_mapping(str_mapping)())

    int1 = forms.ChoiceField(choices=IntegerChoices)
    int2 = forms.ChoiceField(choices=int_tuple)
    int3 = forms.ChoiceField(choices=int_mapping)
    int4 = forms.ChoiceField(choices=int_tuple())
    int5 = forms.ChoiceField(choices=int_mapping())
    int6 = forms.ChoiceField(choices=to_named_seq(int_tuple))
    int7 = forms.ChoiceField(choices=to_named_seq(int_mapping))
    int8 = forms.ChoiceField(choices=to_named_seq(int_tuple)())
    int9 = forms.ChoiceField(choices=to_named_seq(int_mapping)())
