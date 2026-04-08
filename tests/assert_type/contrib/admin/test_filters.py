from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING

from django.contrib.admin.filters import FieldListFilter, ListFilter, SimpleListFilter, _ListFilterChoices
from typing_extensions import assert_type, override

if TYPE_CHECKING:
    from django.contrib.admin.views.main import ChangeList


# Custom ListFilter subclass with a completely different choices() schema.
# The loosened base return type (Mapping[str, object]) allows this.
# This can be useful for user who customized the builtin admin template (`admin/filter.html`) with something
# expecting a different type
class MyListFilter(ListFilter):
    @override
    def choices(self, changelist: ChangeList) -> Iterator[Mapping[str, object]]:
        yield {"label": "All items", "icon": "star", "count": 42, "active": True}


def test_choices(
    changelist: ChangeList,
    base_filter: ListFilter,
    simple_filter: SimpleListFilter,
    field_filter: FieldListFilter,
    custom_filter: MyListFilter,
) -> None:
    # Base ListFilter.choices() returns the loosened type: Iterator[Mapping[str, object]]
    assert_type(base_filter.choices(changelist), Iterator[Mapping[str, object]])

    # SimpleListFilter and FieldListFilter narrow the return type via @override
    assert_type(simple_filter.choices(changelist), Iterator[_ListFilterChoices])
    assert_type(field_filter.choices(changelist), Iterator[_ListFilterChoices])

    # Custom subclass with a completely different schema works without type errors
    assert_type(custom_filter.choices(changelist), Iterator[Mapping[str, object]])
