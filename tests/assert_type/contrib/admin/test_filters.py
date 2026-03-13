from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING

from django.contrib.admin.filters import FieldListFilter, ListFilter, SimpleListFilter, _ListFilterChoices
from typing_extensions import assert_type, override

if TYPE_CHECKING:
    from django.contrib.admin.views.main import ChangeList


class MyFieldListFilter(FieldListFilter):
    def populate(self) -> None:
        # Arbitrary method to showcase that subclasses can store arbitrary values
        # (e.g. list[list[str]] for __in keys) without `type: ignore`,
        # since `ListFilter.used_parameters` is `dict[str, object]`.
        self.used_parameters["state__in"] = [["active", "pending"]]


def test_used_parameters(
    simple_filter: SimpleListFilter,
    field_filter: FieldListFilter,
    custom_filter: MyFieldListFilter,
) -> None:
    # SimpleListFilter narrows used_parameters to dict[str, str]
    assert_type(simple_filter.used_parameters, dict[str, str])

    # FieldListFilter inherits dict[str, object] from ListFilter
    assert_type(field_filter.used_parameters, dict[str, object])

    # Custom subclasses inherit dict[str, object] too
    assert_type(custom_filter.used_parameters, dict[str, object])


# Custom ListFilter subclass with a completely different choices() schema.
# The loosened base return type (Mapping[str, object]) allows this.
# This can be useful for user who customized the builtin admin template (`admin/filter.html`) with something
# expecting a different type
class MyChoicesListFilter(ListFilter):
    @override
    def choices(self, changelist: ChangeList) -> Iterator[Mapping[str, object]]:
        yield {"label": "All items", "icon": "star", "count": 42, "active": True}


def test_choices(
    changelist: ChangeList,
    base_filter: ListFilter,
    simple_filter: SimpleListFilter,
    field_filter: FieldListFilter,
    my_choices_list_filter: MyChoicesListFilter,
) -> None:
    # Base ListFilter.choices() returns the loosened type: Iterator[Mapping[str, object]]
    assert_type(base_filter.choices(changelist), Iterator[Mapping[str, object]])

    # SimpleListFilter and FieldListFilter narrow the return type via @override
    assert_type(simple_filter.choices(changelist), Iterator[_ListFilterChoices])
    assert_type(field_filter.choices(changelist), Iterator[_ListFilterChoices])

    # Custom subclass with a completely different schema works without type errors
    assert_type(my_choices_list_filter.choices(changelist), Iterator[Mapping[str, object]])
